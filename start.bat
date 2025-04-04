@echo off
REM Script simples para descompactar dump_intuitivecare_bd.zip

setlocal

REM Configura caminhos
set ZIP_FILE=BD\dump_intuitivecare_bd.zip
set DESTINO=BD\

echo.
echo Descompactando arquivo %ZIP_FILE%...
echo.

REM Verifica se o arquivo ZIP existe
if not exist "%ZIP_FILE%" (
    echo ERRO: Arquivo %ZIP_FILE% nao encontrado!
    pause
    exit /b 1
)

REM Cria pasta de destino se não existir
if not exist "%DESTINO%" (
    mkdir "%DESTINO%"
)

REM Descompacta usando PowerShell (disponível no Windows 7+)
powershell -command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%DESTINO%' -Force"

if %errorlevel% neq 0 (
    echo ERRO: Falha ao descompactar o arquivo
    pause
    exit /b 1
)

echo.
echo Descompactacao concluida com sucesso!
echo Arquivos extraidos para: %DESTINO%
echo.

REM Lista arquivos extraídos
dir "%DESTINO%"

pause