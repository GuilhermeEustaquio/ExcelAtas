# ExcelAtas

Projeto reorganizado em duas pastas principais:

- `programa_completo/`: scripts Python de processamento (CLI e app desktop).
- `aplicacao_web/`: aplicação web Flask com autenticação de usuários.

## Requisitos (desenvolvimento)

```bash
python -m pip install -r requirements.txt
```

## Aplicação Web

```bash
py -m aplicacao_web.web_app
```

Abra no navegador: `http://localhost:5000`

### Login padrão

- **Usuário administrador:** `eustaquio`
- **Senha:** `eustaquio2005`

Somente esse usuário tem acesso ao botão **Cadastrar usuários** para criar novos logins.

## Aplicação Desktop (desenvolvimento)

```bash
py -m programa_completo.desktop_app
```

> Requer Tkinter disponível no Python da máquina.

## Scripts Originais (CLI)

Gerar planilha:

```bash
python programa_completo/main.py arquivo.pdf -o Relatorio.xlsx
```

Renomear PDF:

```bash
python programa_completo/renomear_pdf_ata.py arquivo.pdf
```
