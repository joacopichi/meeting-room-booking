# Meeting Room Booking System

Una aplicación de consola en Python para gestionar usuarios, salas y reservas de salas de reuniones. Utiliza patrones de diseño Repository y Strategy, y permite validar conflictos de horarios.

## 🚀 Requisitos

- Python 3.10 o superior
- Docker

## ⚡ Instalación y ejecución

### 1. Clonar el repositorio

```sh
git clone <URL_DEL_REPOSITORIO>
cd meeting-room-booking
```

### 2. Ejecutar con Python

Asegúrate de tener Python 3.10+ instalado.

```sh
python -m src/main.py
```

### 3. Ejecutar pruebas unitarias

```sh
python -m unittest discover tests
```

## 🐳 Ejecución con Docker

1. Construye la imagen:

   ```sh
   docker build -t meeting-room-booking .
   ```

2. Ejecuta el contenedor:

   ```sh
   docker run -it meeting-room-booking
   ```

Esto iniciará la aplicación en modo interactivo en la terminal del contenedor.

---

## 📦 Estructura del proyecto

- `src/` - Código fuente principal
- `tests/` - Pruebas unitarias
- `requirements.txt` - Dependencias (vacío, solo estándar)
- `Dockerfile` - Para construir la imagen Docker

---

## ✨ Características

- Gestión de usuarios y salas
- Creación de reservas con validación de solapamiento
- Interfaz de consola sencilla
- Patrones Repository y Strategy
- Pruebas unitarias con `unittest`
- Listo para Docker