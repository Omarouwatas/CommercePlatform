from flask import Blueprint, send_file, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import mongo
from bson import ObjectId
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

receipt_bp = Blueprint("receipt", __name__)

@receipt_bp.route("/<vente_id>", methods=["GET"])
@jwt_required()
def generate_receipt(vente_id):
    vente = mongo.db.ventes.find_one({"_id": ObjectId(vente_id)})
    client = mongo.db.users.find_one({"_id": ObjectId(vente["utilisateur_id"])})
    if not vente:
        return jsonify({"msg": "Vente non trouvée"}), 404

    commande = mongo.db.commandes.find_one({"_id": ObjectId(vente["commande_id"])})
    paiement = mongo.db.paiements.find_one({"vente_id": vente_id})

    filename = f"recu_{vente_id}.pdf"
    filepath = f"/tmp/{filename}"

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, f"Reçu de Vente #{vente_id[:6]}")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(100, y, f"Date : {vente['date'].strftime('%Y-%m-%d %H:%M')}")
    y -= 20
    c.drawString(100, y, f"Nom du client : {client.get('nom', 'Inconnu')}")
    y -= 20
    c.drawString(100, y, f"Mode de paiement : {paiement['methode'] if paiement else 'N/A'}")
    y -= 20

    c.drawString(100, y, f"Statut de la commande : {commande['statut'] if commande else 'non défini'}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, "Produits achetés :")
    y -= 20
    c.setFont("Helvetica", 11)

    for p in commande.get("produits", []):
        nom = p.get("nom", "Produit inconnu")
        quantite = p.get("quantite", 0)
        prix = p.get("prix", 0)
        c.drawString(110, y, f"- {nom} × {quantite} @ {prix}€")
        y -= 18

        if y < 100: 
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, f"Total payé : {vente['total']} €")
    y -= 20

    c.drawString(100, y, "Merci pour votre achat !")
    c.showPage()
    c.save()

    return send_file(filepath, as_attachment=True)
