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

## Hospedar a aplicação web na internet (opção gratuita recomendada)

A melhor opção gratuita para este projeto Flask atualmente é o **PythonAnywhere**.

- Mantém suporte direto a Flask no plano gratuito.
- Não depende de free tier temporário.
- Funciona bem com o banco SQLite já usado no projeto.

### Deploy recomendado

Siga o guia completo em [`DEPLOY_PYTHONANYWHERE.md`](DEPLOY_PYTHONANYWHERE.md).

Resumo rápido:

1. Criar conta no PythonAnywhere.
2. Clonar o repositório no console.
3. Criar virtualenv e instalar `requirements.txt`.
4. Configurar o arquivo WSGI para apontar para `aplicacao_web.web_app`.
5. Definir `SECRET_KEY` e `SESSION_COOKIE_SECURE`.
6. Recarregar a aplicação e acessar a URL `*.pythonanywhere.com`.

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
