#!/usr/bin/env python3
from __future__ import annotations

import os
import sqlite3
import tempfile
from pathlib import Path

from flask import Flask, flash, g, jsonify, redirect, render_template, request, send_file, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from programa_completo.main import process_pdf, save_xlsx
from programa_completo.renomear_pdf_ata import extrair_numero_ata_e_ug, nome_ata

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "usuarios.db"

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-insecure-change-me")
app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"


ADMIN_USERNAME = "eustaquio"
ADMIN_PASSWORD = "eustaquio2005"


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DB_DIR.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    admin = db.execute("SELECT id FROM usuarios WHERE username = ?", (ADMIN_USERNAME,)).fetchone()
    if admin is None:
        db.execute(
            "INSERT INTO usuarios (username, password_hash, is_admin) VALUES (?, ?, 1)",
            (ADMIN_USERNAME, generate_password_hash(ADMIN_PASSWORD)),
        )
    db.commit()
    db.close()


def current_user() -> sqlite3.Row | None:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return get_db().execute("SELECT id, username, is_admin FROM usuarios WHERE id = ?", (user_id,)).fetchone()


def require_login():
    if current_user() is None:
        return redirect(url_for("login"))
    return None


def _save_uploaded_pdf(uploaded) -> tuple[Path, str]:
    if uploaded is None or uploaded.filename is None or uploaded.filename.strip() == "":
        raise ValueError("Selecione um arquivo PDF para continuar.")

    filename = secure_filename(uploaded.filename)
    if not filename.lower().endswith(".pdf"):
        raise ValueError(f"Formato inválido em '{filename}'. Envie apenas arquivos .pdf")

    tmpdir = Path(tempfile.mkdtemp(prefix="excelatas_"))
    pdf_path = tmpdir / filename
    uploaded.save(pdf_path)
    return pdf_path, filename


def _validate_pdf_upload() -> tuple[Path, str]:
    return _save_uploaded_pdf(request.files.get("pdf"))


def _validate_pdf_uploads() -> list[tuple[Path, str]]:
    uploads = [f for f in request.files.getlist("pdf") if f and (f.filename or "").strip()]
    if not uploads:
        raise ValueError("Selecione ao menos um arquivo PDF para continuar.")

    return [_save_uploaded_pdf(uploaded) for uploaded in uploads]


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT id, username, password_hash, is_admin FROM usuarios WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Usuário ou senha inválidos.", "error")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    user = current_user()
    return render_template("index.html", user=user)


@app.route("/usuarios/cadastrar", methods=["GET", "POST"])
def cadastrar_usuario():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    user = current_user()
    if user is None or not user["is_admin"]:
        flash("Somente o administrador pode cadastrar usuários.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Preencha usuário e senha para continuar.", "error")
            return render_template("register.html", user=user)

        try:
            get_db().execute(
                "INSERT INTO usuarios (username, password_hash, is_admin) VALUES (?, ?, 0)",
                (username, generate_password_hash(password)),
            )
            get_db().commit()
            flash(f"Usuário '{username}' cadastrado com sucesso.", "success")
        except sqlite3.IntegrityError:
            flash("Este usuário já existe.", "error")

    return render_template("register.html", user=user)


@app.route("/api/extrair", methods=["POST"])
def api_extrair():
    redirect_response = require_login()
    if redirect_response:
        return jsonify({"erro": "Faça login para continuar."}), 401

    try:
        pdf_path, original_name = _validate_pdf_upload()
        rows = process_pdf(pdf_path)

        if not rows:
            return jsonify({"erro": "Nenhum item de CRO/2 foi encontrado no PDF enviado."}), 422

        xlsx_name = f"Relatorio_{Path(original_name).stem}.xlsx"
        output_path = pdf_path.with_name(xlsx_name)
        save_xlsx(rows, output_path)

        return send_file(output_path, as_attachment=True, download_name=xlsx_name)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"erro": str(exc)}), 400


@app.route("/api/renomear", methods=["POST"])
def api_renomear():
    redirect_response = require_login()
    if redirect_response:
        return jsonify({"erro": "Faça login para continuar."}), 401

    try:
        sugestoes = []
        for pdf_path, original_name in _validate_pdf_uploads():
            numero_ata, ug = extrair_numero_ata_e_ug(pdf_path)

            if not numero_ata or not ug:
                sugestoes.append(
                    {
                        "arquivo_original": original_name,
                        "erro": "Não foi possível identificar número da ata e UG no arquivo.",
                    }
                )
                continue

            sugestoes.append(
                {
                    "arquivo_original": original_name,
                    "numero_ata": numero_ata,
                    "ug": ug,
                    "novo_nome": nome_ata(numero_ata, ug),
                }
            )

        if not sugestoes:
            return jsonify({"erro": "Nenhum arquivo válido foi enviado."}), 422

        return jsonify({"sugestoes": sugestoes})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"erro": str(exc)}), 400


with app.app_context():
    init_db()


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
