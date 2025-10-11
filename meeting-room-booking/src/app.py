import os
import json
import redis
import jwt
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
from src.services.UserService import UserService
from src.services.RoomService import RoomService
from src.services.BookingService import BookingService
from src.repositories.UserRepository import UserRepository
from src.repositories.RoomRepository import RoomRepository
from src.repositories.BookingRepository import BookingRepository
from src.patterns.DefaultValidation import DefaultValidation
from functools import wraps

load_dotenv()

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")

try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True
    )
    redis_client.ping()
    print(f"[INFO] Conectado a Redis en {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    redis_client = None
    print(f"[WARN] No se pudo conectar a Redis: {e}")

user_service = UserService(UserRepository())
room_service = RoomService(RoomRepository())
booking_service = BookingService(BookingRepository(), DefaultValidation())

def validate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Invalid or missing token"}), 401

        token = auth_header.split(" ")[1]

        if not redis_client or not redis_client.exists(f"token:{token}"):
            return jsonify({"message": "Invalid or missing token"}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function

@app.route("/generate-token", methods=["POST"])
def generate_token():
    data = request.json or {}
    user = data.get("user", "default_user")

    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"user": user, "exp": expiration}, SECRET_KEY, algorithm="HS256")

    if redis_client:
        redis_client.setex(f"token:{token}", timedelta(hours=1), "valid")

    return jsonify({"token": token}), 200

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Meeting Room Booking API"}), 200

@app.route("/health", methods=["GET"])
def health():
    argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    local_time = datetime.now(argentina_tz)
    client_ip = request.remote_addr
    payload = {
        "status": "ok",
        "timestamp": local_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "client_ip": client_ip,
    }
    if redis_client:
        redis_client.lpush("health_requests", json.dumps(payload))
    return jsonify(payload), 200

@app.route("/ping", methods=["GET"])
def ping():
    now = datetime.utcnow().isoformat()
    payload = {"status": "pong", "timestamp": now}
    if redis_client:
        redis_client.lpush("ping_requests", json.dumps(payload))
    return jsonify(payload)

@app.route("/get-responses", methods=["GET"])
@validate_token
def get_responses():
    if not redis_client:
        return jsonify({"error": "Redis no disponible"}), 500
    try:
        health_data = redis_client.lrange("health_requests", 0, -1)
        health_data = [json.loads(r) for r in health_data]

        html = "<h2>Health Responses</h2><ul>"
        for r in health_data:
            html += f"<li>{r}</li>"
        html += "</ul>"
        html += """
            <form action="/clear-responses" method="post">
                <button type="submit">Clear All Responses</button>
            </form>
        """
        return html
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear-responses", methods=["POST", "DELETE"])
@validate_token
def clear_responses():
    if not redis_client:
        return jsonify({"error": "Redis no disponible"}), 500
    try:
        redis_client.delete("health_requests")
        redis_client.delete("ping_requests")
        return jsonify({"message": "All responses have been cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400
    user = user_service.create_user(name, email)
    return jsonify(user.__dict__), 201

@app.route("/users", methods=["GET"])
def list_users():
    users = user_service.list_users()
    return jsonify([u.__dict__ for u in users]), 200

@app.route("/rooms", methods=["POST"])
def create_room():
    data = request.json or {}
    name = data.get("name")
    capacity = data.get("capacity")
    try:
        capacity = int(capacity)
    except (TypeError, ValueError):
        return jsonify({"error": "Name and integer capacity required"}), 400
    room = room_service.create_room(name, capacity)
    return jsonify(room.__dict__), 201

@app.route("/rooms", methods=["GET"])
def list_rooms():
    rooms = room_service.list_rooms()
    return jsonify([r.__dict__ for r in rooms]), 200

@app.route("/bookings", methods=["POST"])
def create_booking():
    data = request.json or {}
    try:
        user_id = int(data.get("user_id"))
        room_id = int(data.get("room_id"))
        start_str = data.get("start")
        duration = int(data.get("duration"))

        user = user_service.get_user_by_id(user_id)
        room = room_service.get_room_by_id(room_id)

        if not user:
            return jsonify({"error": "User not found"}), 404
        if not room:
            return jsonify({"error": "Room not found"}), 404

        start_date = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        booking = booking_service.create_booking(user, room, start_date, duration)
        return jsonify(booking.__dict__), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/bookings", methods=["GET"])
def list_bookings():
    bookings = booking_service.list_bookings()
    return jsonify([b.__dict__ for b in bookings]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)