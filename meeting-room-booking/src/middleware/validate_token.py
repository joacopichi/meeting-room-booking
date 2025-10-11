import os
import jwt
import redis
from functools import wraps
from flask import request, jsonify

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")


def validate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Invalid or missing token"}), 401

        token = auth_header.split(" ")[1]

        if not redis_client.exists(f"token:{token}"):
            return jsonify({"message": "Invalid or missing token"}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function
