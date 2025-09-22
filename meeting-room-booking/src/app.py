from flask import Flask, request, jsonify
from src.services.UserService import UserService
from src.services.RoomService import RoomService
from src.services.BookingService import BookingService
from src.repositories.UserRepository import UserRepository
from src.repositories.RoomRepository import RoomRepository
from src.repositories.BookingRepository import BookingRepository
from src.patterns.DefaultValidation import DefaultValidation
from datetime import datetime
import pytz

app = Flask(__name__)

user_service = UserService(UserRepository())
room_service = RoomService(RoomRepository())
booking_service = BookingService(BookingRepository(), DefaultValidation())

@app.route("/health", methods=["GET"])
def health():
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    local_time = datetime.now(argentina_tz)
    
    return jsonify({
        "status": "ok",
        "timestamp": local_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }), 200

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Meeting Room Booking API"}), 200

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
    app.run(debug=True)