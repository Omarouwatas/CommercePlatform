from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import mongo
from bson import ObjectId
from datetime import datetime
from app.utils.auth_utils import get_current_user

products_bp = Blueprint("products", __name__)

def admin_only():
    user = get_current_user()
    if not user or user.get("role") != "admin":
        return False
    return True

@products_bp.route("/", methods=["POST"])
@jwt_required()
def add_product():
    if not admin_only():
        return jsonify({"msg": "Admins only"}), 403

    data = request.get_json()
    if not data.get("name") or not data.get("price") or not data.get("stock"):
        return jsonify({"msg": "name, price, and stock are required"}), 400

    product = {
        "name": data["name"],
        "price": float(data["price"]),
        "stock": int(data["stock"]),
        "created_at": datetime.utcnow()
    }
    mongo.db.products.insert_one(product)
    return jsonify({"msg": "Product added successfully"}), 201

@products_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_products():
    products = list(mongo.db.products.find())
    for p in products:
        p["_id"] = str(p["_id"])
    return jsonify(products), 200

@products_bp.route("/<product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    if not admin_only():
        return jsonify({"msg": "Admins only"}), 403

    data = request.get_json()
    update_fields = {}

    if "name" in data:
        update_fields["name"] = data["name"]
    if "price" in data:
        update_fields["price"] = float(data["price"])
    if "stock" in data:
        update_fields["stock"] = int(data["stock"])

    result = mongo.db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_fields}
    )
    if result.matched_count == 0:
        return jsonify({"msg": "Product not found"}), 404

    return jsonify({"msg": "Product updated successfully"}), 200

@products_bp.route("/<product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    if not admin_only():
        return jsonify({"msg": "Admins only"}), 403

    result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        return jsonify({"msg": "Product not found"}), 404
    return jsonify({"msg": "Product deleted successfully"}), 200
@products_bp.route("/by-category/<categorie>", methods=["GET"])
@jwt_required()
def get_products_by_category(categorie):
    produits = list(mongo.db.products.find({"categorie": categorie}))
    for p in produits:
        p["_id"] = str(p["_id"])
    return jsonify(produits), 200
