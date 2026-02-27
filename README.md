# ExcelAtas

Projeto reorganizado em duas pastas principais:

- `programa_completo/`: scripts Python de processamento (CLI e app desktop).
- `aplicacao_web/`: aplicação web Flask com autenticação de usuários.

## Requisitos (desenvolvimento)

```bash
python -m pip install -r requirements.txt
```

## Aplicação Web (local)

```bash
py -m aplicacao_web.web_app
```

Abra no navegador: `http://localhost:5000`

### Login padrão

- **Usuário administrador:** `eustaquio`
- **Senha:** `eustaquio2005`

Somente esse usuário tem acesso ao botão **Cadastrar usuários** para criar novos logins.

## Hospedar a aplicação web na internet (Render)

Este projeto já está preparado para deploy com **Gunicorn** usando os arquivos `Procfile` e `wsgi.py`.

### 1) Suba o projeto no GitHub

```bash
git push origin <sua-branch>
```

### 2) Crie um serviço Web no Render

1. Acesse https://render.com e clique em **New +** → **Web Service**.
2. Conecte seu repositório.
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`

### 3) Defina variáveis de ambiente

No painel do Render, em **Environment Variables**, configure:

- `SECRET_KEY` = uma chave forte e única (obrigatório em produção)
- `SESSION_COOKIE_SECURE` = `1`

> O Render já injeta a variável `PORT` automaticamente.

### 4) Deploy

Clique em **Create Web Service**. Após finalizar o deploy, o Render vai disponibilizar uma URL pública `https://...onrender.com`.

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
