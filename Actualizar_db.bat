@echo off

:: Ruta al directorio del entorno virtual
set "venv_path=C:\Users\Usuario\Proyectos\BD_Monitoreo\venv"

:: Activa el entorno virtual
call "%venv_path%\Scripts\activate"

:: Ruta al archivo Python que deseas ejecutar
set "python_script=C:\Users\Usuario\Proyectos\BD_Monitoreo\src\hist_poo\act_db_poo.py"

:: Ejecuta el programa de Python
python "%python_script%"

:: Desactiva el entorno virtual
call "%venv_path%\Scripts\deactivate"

:: Pausa la ejecución para mantener la ventana abierta
pause