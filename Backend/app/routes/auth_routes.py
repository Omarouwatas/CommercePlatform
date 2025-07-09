from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime
from app.extensions import mongo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    required_fields = ["email", "password", "nom"]
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Email, password and nom are required"}), 400

    email = data["email"]
    password = data["password"]
    nom = data["nom"]
    role = data.get("role", "client")
    adresse = data.get("adresse", "")
    telephone = data.get("telephone", "")

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    new_user = {
        "email": email,
        "password": hashed_password,
        "nom": nom,
        "role": role,
        "adresse": adresse,
        "telephone": telephone,
        "date_inscription": datetime.utcnow()
    }

    mongo.db.users.insert_one(new_user)
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email and password are required"}), 400

    user = mongo.db.users.find_one({"email": data["email"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(hours=24))
    return jsonify({
        "access_token": access_token,
        "nom": user.get("nom"),
        "role": user.get("role")
    }), 200
