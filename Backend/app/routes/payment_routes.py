from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId
from app.extensions import mongo
from datetime import datetime
import stripe

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/stripe", methods=["POST"])
@jwt_required()
def payer_avec_stripe():
    data = request.get_json()
    commande_id = data.get("commande_id")
    token = data.get("token")  
    if not commande_id or not token:
        return jsonify({"msg": "commande_id and token are required"}), 400

    commande = mongo.db.commandes.find_one({"_id": ObjectId(commande_id)})
    if not commande:
        return jsonify({"msg": "Commande non trouvée"}), 404

    montant = int(commande["total"] * 100) 
    try:
        charge = stripe.Charge.create(
            amount=montant,
            currency="eur",
            description=f"Commande {commande_id}",
            source=token
        )
    except stripe.error.StripeError as e:
        return jsonify({"msg": "Erreur Stripe", "error": str(e)}), 402

    vente = {
        "commande_id": commande_id,
        "utilisateur_id": commande["client_id"],
        "date": datetime.utcnow(),
        "total": commande["total"],
        "statut": "validée"
    }
    result_vente = mongo.db.ventes.insert_one(vente)
    vente_id = str(result_vente.inserted_id)

    paiement = {
        "vente_id": vente_id,
        "commande_id": commande_id,
        "montant": commande["total"],
        "methode": "stripe",
        "statut": "effectué",
        "date_paiement": datetime.utcnow(),
        "stripe_charge_id": charge["id"]
    }
    mongo.db.paiements.insert_one(paiement)

    mongo.db.commandes.update_one({"_id": ObjectId(commande_id)}, {"$set": {"statut": "payée", "vente_id": vente_id}})

    return jsonify({"msg": "Paiement réussi et vente enregistrée", "vente_id": vente_id}), 200
@payment_bp.route("/cash", methods=["POST"])
@jwt_required()
def payer_en_especes():
    data = request.get_json()
    commande_id = data.get("commande_id")

    if not commande_id:
        return jsonify({"msg": "commande_id is required"}), 400

    commande = mongo.db.commandes.find_one({"_id": ObjectId(commande_id)})
    if not commande:
        return jsonify({"msg": "Commande non trouvée"}), 404

    montant = commande.get("total", 0.0)
    vente = {
        "commande_id": commande_id,
        "utilisateur_id": commande["client_id"],
        "date": datetime.utcnow(),
        "total": montant,
        "statut": "validée"
    }
    vente_result = mongo.db.ventes.insert_one(vente)
    vente_id = str(vente_result.inserted_id)

    paiement = {
        "vente_id": vente_id,
        "commande_id": commande_id,
        "montant": montant,
        "methode": "espèces",
        "statut": "effectué",
        "date_paiement": datetime.utcnow()
    }
    mongo.db.paiements.insert_one(paiement)

    mongo.db.commandes.update_one({"_id": ObjectId(commande_id)}, {"$set": {"statut": "payée", "vente_id": vente_id}})

    return jsonify({"msg": "Paiement en espèces enregistré", "vente_id": vente_id}), 201
