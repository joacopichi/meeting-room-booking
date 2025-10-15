# Sistema de Reservas de Salas de Reunión

Aplicación **Flask** en Python para la gestión de usuarios, salas de reuniones y reservas, implementando los patrones de diseño **Repository** y **Strategy**, autenticación con **JWT** y almacenamiento temporal en **Redis**. Incluye validación de conflictos de reservas, endpoints para logs y limpieza, y protección de rutas.

---

## Tabla de Contenidos

1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
5. [Ejecución Local](#ejecución-local)
6. [Ejecución con Docker](#ejecución-con-docker)
7. [Estructura del Proyecto](#estructura-del-proyecto)
8. [Funcionalidades](#funcionalidades)
9. [Endpoints de la API](#endpoints-de-la-api)
10. [Pruebas con Postman](#pruebas-con-postman)
11. [Testing](#testing)
12. [CI/CD](#cicd)
13. [Notas Adicionales](#notas-adicionales)

---

## Descripción

API RESTful desarrollada con **Flask** para gestionar usuarios, salas y reservas de reuniones. Utiliza **JWT** para autenticación, **Redis** para almacenamiento temporal de logs y respuestas, y patrones **Repository** y **Strategy** para una arquitectura escalable y mantenible.

---

## Requisitos

- Python 3.10 o superior
- Redis (servidor local o remoto)
- Docker (opcional)
- pip

---

## Instalación

1. **Clonar el repositorio**

   ```sh
   git clone <REPOSITORY_URL>
   cd meeting-room-booking
   ```

2. **Instalar dependencias**

   ```sh
   pip install -r requirements.txt
   ```

3. **Configurar Redis**

   - Instala y ejecuta Redis localmente (`redis-server`) o usa un servicio remoto.
   - Configura la URL de Redis en las variables de entorno.

---

## Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
FLASK_APP=src/app.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta
JWT_SECRET_KEY=tu_jwt_secreto
REDIS_URL=redis://localhost:6379/0
```

---

## Ejecución Local

Desde la raíz del proyecto, ejecuta:

```sh
python -m src.app
```

La API estará disponible en `http://localhost:5000`.

---

## Ejecución con Docker

1. **Construir la imagen**

   ```sh
   docker build -t meeting-room-booking .
   ```

2. **Ejecutar el contenedor**

   ```sh
   docker run -it --env-file .env meeting-room-booking
   ```

---

## Estructura del Proyecto

```.
meeting-room-booking/
│
├── src/                # Código fuente principal
│   ├── app.py          # Punto de entrada Flask
│   ├── main.py         # Alternativa de ejecución
│   ├── models/         # Modelos de dominio
│   ├── repositories/   # Lógica de acceso a datos (Repository)
│   ├── patterns/       # Estrategias de validación (Strategy)
│   ├── services/       # Lógica de negocio
│   ├── middleware/     # Validación de token JWT
│   └── ...             # Otros módulos
│
├── tests/              # Pruebas unitarias
│
├── requirements.txt    # Dependencias
├── Dockerfile          # Imagen Docker
├── .env                # Variables de entorno
├── docker-compose.yml  # Orquestación opcional
└── README.md           # Documentación
```

---

## Funcionalidades

- **Gestión de usuarios**: crear y listar usuarios.
- **Gestión de salas**: crear y listar salas de reunión.
- **Reservas**: crear reservas con validación de conflictos de horario.
- **Autenticación JWT**: protección de endpoints.
- **Logs y respuestas**: endpoints para obtener y limpiar logs/respuestas en Redis.
- **Patrones Repository y Strategy**: arquitectura desacoplada y extensible.
- **Healthcheck y ping**: endpoints para monitoreo.

---

## Endpoints de la API

### 1. `/users`
- **GET**: Listar usuarios.
- **POST**: Crear usuario.
- **Headers**: `Authorization: Bearer <token>`
- **Ejemplo respuesta**:
    ```json
    [
      {"id": 1, "username": "juan"}
    ]
    ```

### 2. `/rooms`
- **GET**: Listar salas.
- **POST**: Crear sala.
- **Headers**: `Authorization: Bearer <token>`
- **Ejemplo respuesta**:
    ```json
    [
      {"id": 1, "name": "Sala A"}
    ]
    ```

### 3. `/bookings`
- **GET**: Listar reservas.
- **POST**: Crear reserva (valida conflictos).
- **DELETE**: Eliminar reserva.
- **Headers**: `Authorization: Bearer <token>`
- **Ejemplo respuesta**:
    ```json
    [
      {
        "id": 1,
        "user_id": 1,
        "room_id": 1,
        "start": "2025-10-15T10:00:00",
        "end": "2025-10-15T11:00:00"
      }
    ]
    ```

### 4. `/generate-token`
- **POST**: Genera un JWT para autenticación.
- **Body**:
    ```json
    {
      "username": "juan"
    }
    ```
- **Ejemplo respuesta**:
    ```json
    {
      "token": "<jwt_token>"
    }
    ```

### 5. `/get-responses`
- **GET**: Obtiene logs/respuestas almacenadas en Redis.
- **Headers**: `Authorization: Bearer <token>`
- **Ejemplo respuesta**:
    ```json
    [
      {"endpoint": "/users", "response": "..."}
    ]
    ```

### 6. `/clear-responses`
- **POST**: Limpia los logs/respuestas en Redis.
- **Headers**: `Authorization: Bearer <token>`
- **Ejemplo respuesta**:
    ```json
    {"message": "Respuestas limpiadas"}
    ```

### 7. `/health`
- **GET**: Verifica el estado de la aplicación.
- **Ejemplo respuesta**:
    ```json
    {"status": "ok"}
    ```

### 8. `/ping`
- **GET**: Prueba de conectividad.
- **Ejemplo respuesta**:
    ```json
    {"message": "pong"}
    ```

---

## Pruebas con Postman

1. **Generar token JWT**
    - Enviar `POST` a `/generate-token` con el usuario.
    - Copiar el token de la respuesta.

2. **Usar el token**
    - En cada request, agregar el header:
      ```
      Authorization: Bearer <jwt_token>
      ```

3. **Probar endpoints**
    - Crear usuarios/salas/reservas con `POST`.
    - Listar con `GET`.
    - Eliminar reservas con `DELETE`.
    - Limpiar logs con `POST` a `/clear-responses`.

---

## Testing

Ejecuta las pruebas unitarias con:

```sh
python -m unittest discover tests
```
o
```sh
pytest tests/
```

---

## CI/CD

El proyecto incluye flujo de integración continua con GitHub Actions (`ci.yml`), ejecutando tests automáticamente en cada push/pull request.

---

## Notas Adicionales

- **Buenas prácticas**: Mantén tus claves secretas fuera del código fuente.
- **Advertencia**: No uses variables de entorno de desarrollo en producción.
- **Redis**: Asegúrate de que Redis esté corriendo antes de iniciar la app.
- **Extensibilidad**: El uso de Repository y Strategy permite agregar nuevas reglas y fuentes de datos fácilmente.
