FROM python:3.11-slim

WORKDIR /app

# Copiamos requirements e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la app
COPY . .

# Exponemos el puerto de Flask
EXPOSE 5000

# Variables de entorno para Flask
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Comando para iniciar Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]