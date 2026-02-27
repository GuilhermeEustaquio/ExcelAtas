@echo off
setlocal EnableExtensions

where python >nul 2>&1
if errorlevel 1 (
  echo Python nao encontrado no PATH.
  echo Instale o Python apenas na maquina de build e execute novamente.
  exit /b 1
)

echo [1/4] Instalando dependencias de build...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto :error

echo [2/4] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist release rmdir /s /q release
if exist ExcelAtas.spec del /q ExcelAtas.spec

echo [3/4] Gerando EXE unico (sem depender de Python instalado)...
py -m PyInstaller --noconfirm --clean --onefile --windowed --name ExcelAtas programa_completo\desktop_app.py
if errorlevel 1 goto :error

echo [4/4] Montando pacote portatil para distribuicao...
mkdir release\ExcelAtas-Windows-Portable
copy /y dist\ExcelAtas.exe release\ExcelAtas-Windows-Portable\ExcelAtas.exe >nul
(
  echo @echo off
  echo cd /d %%~dp0
  echo start "" "ExcelAtas.exe"
) > release\ExcelAtas-Windows-Portable\INICIAR_EXCELATAS.bat
(
  echo ExcelAtas - pacote portatil para Windows
  echo.
  echo 1^) Extraia a pasta em qualquer local.
  echo 2^) Execute INICIAR_EXCELATAS.bat com duplo clique.
  echo.
  echo Nao e necessario instalar Python na maquina final.
) > release\ExcelAtas-Windows-Portable\LEIA-ME.txt

echo.
echo Concluido!
echo EXE: dist\ExcelAtas.exe
echo Pacote para entrega: release\ExcelAtas-Windows-Portable

goto :end

:error
echo Falha ao gerar EXE.
exit /b 1

:end
endlocal
