from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.extensions import mongo
from datetime import datetime

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")
    quantite = int(data.get("quantite", 1))

    if not product_id:
        return jsonify({"msg": "product_id is required"}), 400

    panier = mongo.db.paniers.find_one({"utilisateur_id": user_id})

    if not panier:
        panier = {
            "utilisateur_id": user_id,
            "elements": [{"product_id": product_id, "quantite": quantite}],
            "date_creation": datetime.utcnow()
        }
        mongo.db.paniers.insert_one(panier)
    else:
        # Mise à jour : ajouter ou incrémenter
        found = False
        for elem in panier["elements"]:
            if elem["product_id"] == product_id:
                elem["quantite"] += quantite
                found = True
        if not found:
            panier["elements"].append({"product_id": product_id, "quantite": quantite})
        mongo.db.paniers.update_one({"_id": panier["_id"]}, {"$set": {"elements": panier["elements"]}})

    return jsonify({"msg": "Produit ajouté au panier"}), 200

@cart_bp.route("/remove", methods=["POST"])
@jwt_required()
def remove_from_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"msg": "product_id is required"}), 400

    panier = mongo.db.paniers.find_one({"utilisateur_id": user_id})
    if not panier:
        return jsonify({"msg": "Panier introuvable"}), 404

    panier["elements"] = [e for e in panier["elements"] if e["product_id"] != product_id]
    mongo.db.paniers.update_one({"_id": panier["_id"]}, {"$set": {"elements": panier["elements"]}})
    return jsonify({"msg": "Produit retiré du panier"}), 200

@cart_bp.route("/", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    panier = mongo.db.paniers.find_one({"utilisateur_id": user_id})
    if not panier:
        return jsonify({"elements": []}), 200

    panier["_id"] = str(panier["_id"])
    return jsonify(panier), 200
