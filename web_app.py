#!/usr/bin/env python3
from __future__ import annotations

import tempfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

from main import process_pdf, save_xlsx
from renomear_pdf_ata import extrair_numero_ata_e_ug, nome_ata

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB


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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/extrair", methods=["POST"])
def api_extrair():
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
    try:
        sugestoes = []
        for pdf_path, original_name in _validate_pdf_uploads():
            numero_ata, ug = extrair_numero_ata_e_ug(pdf_path)

            if not numero_ata or not ug:
                sugestoes.append({
                    "arquivo_original": original_name,
                    "erro": "Não foi possível identificar número da ata e UG no arquivo.",
                })
                continue

            sugestoes.append({
                "arquivo_original": original_name,
                "numero_ata": numero_ata,
                "ug": ug,
                "novo_nome": nome_ata(numero_ata, ug),
            })

        if not sugestoes:
            return jsonify({"erro": "Nenhum arquivo válido foi enviado."}), 422

        return jsonify({"sugestoes": sugestoes})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"erro": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
