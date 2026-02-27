@echo off
setlocal

echo [1/3] Instalando dependencias de build...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto :error

echo [2/3] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ExcelAtas.spec del /q ExcelAtas.spec

echo [3/3] Gerando EXE unico (sem depender de Python instalado)...
pyinstaller --noconfirm --clean --onefile --windowed --name ExcelAtas desktop_app.py
if errorlevel 1 goto :error

echo.
echo Concluido! EXE gerado em: dist\ExcelAtas.exe
goto :end

:error
echo Falha ao gerar EXE.
exit /b 1

:end
endlocal
