import jwt
import datetime
from flask import Blueprint, request, jsonify

SECRET_KEY = "44725639-2a35-4741-bc9b-02a77510154a"  # We can change to env var for better security, this is just an example

# Example of hardcoded users, on real life we can create a database for this info
USERS = {
    "admin_user": {"password": "admin123", "role": "admin"},
    "normal_user": {"password": "user123", "role": "user"}
}

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint to authenticate user and get permissions.
    """
    auth_data = request.json
    username = auth_data.get('username')
    password = auth_data.get('password')

    # Validate credentials
    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "username": username,
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token}), 200
