# ExcelAtas

Interface web e desktop para usar os dois programas Python do projeto:

- Extração de itens da CRO/2 de PDF para XLSX.
- Renomeação padronizada de PDFs de atas.

## Requisitos

```bash
python -m pip install flask openpyxl pdfplumber pypdf
```

## Aplicação Web

```bash
python web_app.py
```

Abra no navegador: `http://localhost:5000`

## Aplicação Desktop

```bash
python desktop_app.py
```

> Requer Tkinter disponível no Python da máquina.

## Scripts Originais (CLI)

Gerar planilha:

```bash
python main.py arquivo.pdf -o Relatorio.xlsx
```

Renomear PDF:

```bash
python renomear_pdf_ata.py arquivo.pdf
```
