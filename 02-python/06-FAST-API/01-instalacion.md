# Instalación de variables de entorno

python -m venv venv



# Permisos

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser



# Activación de las variables de entorno

.\venv\Scripts\activate



# Instalamos FASTAPI

pip install "fastapi[standard]" uvicorn



# Arrancamos el server:

fastapi dev main.py



# Reload del server:

uvicorn main:app --reload


