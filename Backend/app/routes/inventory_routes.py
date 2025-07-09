from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import mongo
from bson import ObjectId
from datetime import datetime

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/", methods=["POST"])
@jwt_required()
def add_inventory():
    data = request.get_json()
    if not data.get("product_id") or not data.get("quantite_disponible") or not data.get("emplacement"):
        return jsonify({"msg": "product_id, quantite_disponible, emplacement are required"}), 400

    inventory = {
        "product_id": data["product_id"],
        "quantite_disponible": int(data["quantite_disponible"]),
        "emplacement": data["emplacement"],
        "date_ajout": datetime.utcnow()
    }
    mongo.db.inventaire.insert_one(inventory)
    return jsonify({"msg": "Inventaire ajouté avec succès"}), 201

@inventory_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_inventory():
    inventaire = list(mongo.db.inventaire.find())
    for i in inventaire:
        i["_id"] = str(i["_id"])
    return jsonify(inventaire), 200

@inventory_bp.route("/produit/<product_id>", methods=["GET"])
@jwt_required()
def get_inventory_by_product(product_id):
    inventaire = list(mongo.db.inventaire.find({"product_id": product_id}))
    for i in inventaire:
        i["_id"] = str(i["_id"])
    return jsonify(inventaire), 200
