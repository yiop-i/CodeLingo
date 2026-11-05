@echo off
rem -------------------------------------------------
rem   Script para iniciar CodeLingo en Windows
rem -------------------------------------------------
rem Si tienes un entorno virtual llamado venv en la carpeta
rem (recomendado), lo activamos primero.
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Aviso: no se encontró entorno virtual. Usando Python del sistema.
)
rem Instalar dependencias si aún no están instaladas
pip install -r requirements.txt

rem Ejecutar la aplicación
python main.py
