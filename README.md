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

## Hospedagem gratuita da aplicação web (PythonAnywhere)

Se você precisa de **hospedagem gratuita**, use o **PythonAnywhere (plano Free)**.

> Dica: o comando `py -m ...` é para Windows. No PythonAnywhere (Linux), use `python3.10 -m ...`.

### 1) Suba o projeto no GitHub

```bash
git push origin <sua-branch>
```

### 2) Crie conta e abra um Bash no PythonAnywhere

1. Acesse https://www.pythonanywhere.com/ e crie uma conta gratuita.
2. No painel, abra um **Bash console**.

### 3) Clone o projeto e instale dependências

```bash
git clone <URL_DO_REPOSITORIO>
cd ExcelAtas
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) Criar Web App Flask (manual configuration)

1. Vá em **Web** → **Add a new web app**.
2. Escolha **Manual configuration** e a versão do Python.
3. Em **WSGI configuration file**, aponte para o projeto adicionando:

```python
import sys
path = '/home/SEU_USUARIO/ExcelAtas'
if path not in sys.path:
    sys.path.append(path)

from aplicacao_web.web_app import app as application
```

### 5) Configure variáveis e recarregue

No arquivo WSGI do PythonAnywhere, antes do import da aplicação, adicione:

```python
import os
os.environ['SECRET_KEY'] = 'troque-por-uma-chave-forte'
os.environ['SESSION_COOKIE_SECURE'] = '1'
```

Depois clique em **Reload** na aba Web.

> Observação: no plano gratuito do PythonAnywhere pode haver limitações (domínio `*.pythonanywhere.com`, hibernação/recursos reduzidos), mas funciona sem custo.

### 6) Teste a URL pública

Após o reload, abra a URL informada na aba Web do PythonAnywhere (formato `https://SEU_USUARIO.pythonanywhere.com`).

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
