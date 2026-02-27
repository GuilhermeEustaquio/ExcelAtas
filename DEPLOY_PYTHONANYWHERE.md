# Deploy gratuito no PythonAnywhere

Este projeto Flask pode ser hospedado gratuitamente no **PythonAnywhere** (plano gratuito),
que é uma opção mais estável para apps Python do que alternativas que removeram free tier.

## 1) Criar conta e subir o código

1. Crie sua conta em https://www.pythonanywhere.com/
2. No painel, abra **Consoles** → **Bash**
3. Clone seu repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd ExcelAtas
```

## 2) Criar virtualenv e instalar dependências

No console Bash do PythonAnywhere:

```bash
mkvirtualenv --python=python3.11 excelatas-env
workon excelatas-env
pip install -r requirements.txt
```

## 3) Criar aplicação web Flask

1. Vá em **Web** → **Add a new web app**
2. Escolha o domínio gratuito `seuusuario.pythonanywhere.com`
3. Selecione **Manual configuration** e Python 3.11

## 4) Configurar WSGI

No painel **Web**, abra o arquivo **WSGI configuration file** e substitua pelo conteúdo abaixo
(adaptando o caminho `/home/seuusuario/ExcelAtas` para o seu usuário):

```python
import os
import sys

project_home = '/home/seuusuario/ExcelAtas'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault('SECRET_KEY', 'troque-esta-chave-em-producao')
os.environ.setdefault('SESSION_COOKIE_SECURE', '1')

from aplicacao_web.web_app import app as application
```

## 5) Configurar virtualenv no painel

Em **Web** → **Virtualenv**, informe o caminho:

```text
/home/seuusuario/.virtualenvs/excelatas-env
```

## 6) Recarregar e testar

1. Clique em **Reload** na página **Web**.
2. Abra `https://seuusuario.pythonanywhere.com/login`.

## Observações

- O banco SQLite (`aplicacao_web/data/usuarios.db`) fica salvo no filesystem da conta.
- Em cada atualização de código, rode `git pull` no console e depois **Reload** na Web tab.
- Troque `SECRET_KEY` por uma chave forte, exclusiva do seu app.
