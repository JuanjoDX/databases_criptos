@echo off

:: Ruta al directorio del entorno virtual
set "venv_path=C:\Users\juanj\Proyectos\databases_criptos\venv"

:: Activa el entorno virtual
call "%venv_path%\Scripts\activate"

:: Ruta al archivo Python que deseas ejecutar
set "python_script=C:\Users\juanj\Proyectos\databases_criptos\src\hist_poo\act_db.py"

:: Define la variable que deseas pasar al script de Python
set "temporalidades=4h" 

:: Ejecuta el programa de Python con la variable como argumento
python "%python_script%" %temporalidades%

:: Desactiva el entorno virtual
call "%venv_path%\Scripts\deactivate"

:: Pausa la ejecución para mantener la ventana abierta
pause