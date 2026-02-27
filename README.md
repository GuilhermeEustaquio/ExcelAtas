# ExcelAtas

Interface web e desktop para usar os dois programas Python do projeto:

- Extração de itens da CRO/2 de PDF para XLSX.
- Renomeação padronizada de PDFs de atas.

## Requisitos

```bash
python -m pip install -r requirements.txt
```

## Aplicação Web

```bash
python web_app.py
```

Abra no navegador: `http://localhost:5000`

### Melhorias da UI

- Botão de seleção de PDF com estilo personalizado.
- Módulo **Documentos** aceitando múltiplos PDFs.
- Lista de sugestões no formato: `arquivo_original.pdf → nome_sugerido.pdf`.

## Aplicação Desktop

```bash
python desktop_app.py
```

> Requer Tkinter disponível no Python da máquina.

## Gerar EXE para Windows (sem instalar dependências na máquina final)

No Windows, execute:

```bat
build_windows_exe.bat
```

Isso gera `dist\ExcelAtas.exe` (arquivo único), que pode ser copiado para outra máquina Windows sem precisar instalar Python ou pacotes separadamente.

## Scripts Originais (CLI)

Gerar planilha:

```bash
python main.py arquivo.pdf -o Relatorio.xlsx
```

Renomear PDF:

```bash
python renomear_pdf_ata.py arquivo.pdf
```
