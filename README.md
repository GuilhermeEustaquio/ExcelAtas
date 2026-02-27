# ExcelAtas

Interface web e desktop para usar os dois programas Python do projeto:

- Extração de itens da CRO/2 de PDF para XLSX.
- Renomeação padronizada de PDFs de atas.

## Requisitos (apenas para desenvolvimento)

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

## Aplicação Desktop (desenvolvimento)

```bash
python desktop_app.py
```

> Requer Tkinter disponível no Python da máquina.

## Entrega para usuários finais no Windows (sem instalar Python)

Se a ideia é entregar para qualquer pessoa abrir e usar sem conhecimento técnico, use o empacotamento abaixo em **uma máquina de build** (somente quem gera o executável precisa de Python):

```bat
build_windows_exe.bat
```

Saídas:

- `dist\ExcelAtas.exe` → executável único.
- `release\ExcelAtas-Windows-Portable\` → pasta pronta para distribuir, contendo:
  - `ExcelAtas.exe`
  - `INICIAR_EXCELATAS.bat` (duplo clique para abrir)
  - `LEIA-ME.txt`

Na máquina final do usuário, basta extrair a pasta e executar `INICIAR_EXCELATAS.bat`.

## Scripts Originais (CLI)

Gerar planilha:

```bash
python main.py arquivo.pdf -o Relatorio.xlsx
```

Renomear PDF:

```bash
python renomear_pdf_ata.py arquivo.pdf
```
