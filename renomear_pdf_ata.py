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


def extrair_numero_ata(pdf_path: Path) -> Optional[str]:
    for page_text in extract_pages_text(pdf_path):
        texto = norm(page_text)
        if not texto:
            continue
        match = RE_ATA_NUM.search(texto)
        if match:
            return match.group(1)
    return None


def nome_ata(numero_ata: str) -> str:
    numero_sanitizado = numero_ata.replace("/", "-")
    return f"ATA_{numero_sanitizado}.pdf"


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

    numero_ata = extrair_numero_ata(pdf_path)
    if not numero_ata:
        raise RuntimeError("Não foi possível encontrar o número da ata no PDF.")

    destino = proximo_nome_disponivel(pdf_path.with_name(nome_ata(numero_ata)))

    if not dry_run:
        pdf_path.rename(destino)

    return destino


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Renomeia um PDF com base no número da ata encontrado no conteúdo."
    )
    parser.add_argument("pdf", type=Path, help="PDF com nome aleatório")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o novo nome sem renomear o arquivo.",
    )
    args = parser.parse_args()

    try:
        novo_caminho = renomear_pdf(args.pdf, dry_run=args.dry_run)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(str(exc)) from exc

    acao = "Novo nome sugerido" if args.dry_run else "Arquivo renomeado para"
    print(f"{acao}: {novo_caminho}")


if __name__ == "__main__":
    main()
