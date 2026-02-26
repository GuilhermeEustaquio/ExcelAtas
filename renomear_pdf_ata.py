#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterator, Optional


def extract_pages_text(pdf_path: Path) -> Iterator[str]:
    try:
        import pdfplumber  # type: ignore

        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                yield page.extract_text() or ""
        return
    except Exception:
        pass

    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            yield page.extract_text() or ""
    except Exception as exc:
        raise RuntimeError("Não foi possível ler o PDF. Instale 'pdfplumber' ou 'pypdf'.") from exc


def norm(s: str) -> str:
    s = (s or "").replace("\u00a0", " ").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


RE_ATA_NUM = re.compile(r"\bn[ºo]\s*([0-9]{1,6}/[0-9]{4})\b", re.IGNORECASE)
RE_UG = re.compile(r"\bUnidade\s+Gerenciadora\s+([0-9]{6})\b", re.IGNORECASE)


def extrair_numero_ata_e_ug(pdf_path: Path) -> tuple[Optional[str], Optional[str]]:
    numero_ata: Optional[str] = None
    ug: Optional[str] = None

    for page_text in extract_pages_text(pdf_path):
        texto = norm(page_text)
        if not texto:
            continue

        if numero_ata is None:
            match_ata = RE_ATA_NUM.search(texto)
            if match_ata:
                numero_ata = match_ata.group(1)

        if ug is None:
            match_ug = RE_UG.search(texto)
            if match_ug:
                ug = match_ug.group(1)

        if numero_ata and ug:
            return numero_ata, ug

    return numero_ata, ug


def nome_ata(numero_ata: str, ug: str) -> str:
    numero_sanitizado = numero_ata.replace("/", "-")
    return f"ATA_{numero_sanitizado}_UG-{ug}.pdf"


def proximo_nome_disponivel(destino: Path) -> Path:
    if not destino.exists():
        return destino

    stem = destino.stem
    suffix = destino.suffix
    pasta = destino.parent

    contador = 1
    while True:
        candidato = pasta / f"{stem}_{contador}{suffix}"
        if not candidato.exists():
            return candidato
        contador += 1


def renomear_pdf(pdf_path: Path, dry_run: bool = False) -> Path:
    if not pdf_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("O arquivo informado não é um PDF.")

    numero_ata, ug = extrair_numero_ata_e_ug(pdf_path)
    if not numero_ata:
        raise RuntimeError("Não foi possível encontrar o número da ata no PDF.")
    if not ug:
        raise RuntimeError("Não foi possível encontrar a Unidade Gerenciadora (UG) no PDF.")

    destino = proximo_nome_disponivel(pdf_path.with_name(nome_ata(numero_ata, ug)))

    if not dry_run:
        pdf_path.rename(destino)

    return destino


def renomear_todos_pdfs_da_pasta(pasta: Path, dry_run: bool = False) -> int:
    if not pasta.exists() or not pasta.is_dir():
        raise NotADirectoryError(f"Pasta inválida: {pasta}")

    pdfs = sorted(pasta.glob("*.pdf"))
    if not pdfs:
        print(f"Nenhum PDF encontrado em: {pasta}")
        return 0

    sucesso = 0
    for pdf in pdfs:
        try:
            destino = renomear_pdf(pdf, dry_run=dry_run)
            acao = "Novo nome sugerido" if dry_run else "Arquivo renomeado para"
            print(f"[{pdf.name}] {acao}: {destino.name}")
            sucesso += 1
        except Exception as exc:  # noqa: BLE001
            print(f"[{pdf.name}] ERRO: {exc}")

    return sucesso


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Renomeia um ou todos os PDFs com base no número da ata e UG encontrados no conteúdo."
    )
    parser.add_argument(
        "alvo",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Arquivo PDF ou pasta com PDFs (padrão: pasta atual)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o novo nome sem renomear o arquivo.",
    )
    args = parser.parse_args()

    try:
        if args.alvo.is_dir():
            total = renomear_todos_pdfs_da_pasta(args.alvo, dry_run=args.dry_run)
            print(f"Processamento concluído. PDFs processados com sucesso: {total}")
            return

        novo_caminho = renomear_pdf(args.alvo, dry_run=args.dry_run)
        acao = "Novo nome sugerido" if args.dry_run else "Arquivo renomeado para"
        print(f"{acao}: {novo_caminho}")
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
