import jwt
from flask import request, jsonify
import functools

SECRET_KEY = "44725639-2a35-4741-bc9b-02a77510154a"  # We can change to env var for better security, this is just an example

def require_jwt(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]

        try:
            # Validate token
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)
    return wrapper

def require_role(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Unauthorized"}), 401

            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if payload.get("role") != role:
                    return jsonify({"error": "Forbidden: insufficient permissions"}), 403
                request.user = payload  # Adiciona os dados do usuário ao objeto `request`
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return func(*args, **kwargs)
        return wrapper
    return decorator
