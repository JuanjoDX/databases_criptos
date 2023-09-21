@echo off

:: Ruta al directorio del entorno virtual
set "venv_path=.\venv"

:: Activa el entorno virtual
call "%venv_path%\Scripts\activate"

:: Ruta al archivo Python que deseas ejecutar
set "python_script=.\src\hist_poo\act_db.py"

:: Ejecuta el programa de Python
python "%python_script%"

:: Desactiva el entorno virtual
call "%venv_path%\Scripts\deactivate"

:: Pausa la ejecución para mantener la ventana abierta
pause