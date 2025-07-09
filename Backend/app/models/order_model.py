from bson import ObjectId
from datetime import datetime

class Commande:
    def __init__(self, client_id, type_commande, frais_livraison=0.0, produits=None, statut="en_attente", date_commande=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.client_id = client_id
        self.type_commande = type_commande  
        self.frais_livraison = float(frais_livraison)
        self.produits = produits if produits else []
        self.date_commande = date_commande if date_commande else datetime.utcnow()
        self.statut = statut

    def calculer_total(self):
        total = sum(item["quantite"] * item["prix"] for item in self.produits)
        return round(total + self.frais_livraison, 2)

    def to_dict(self):
        return {
            "_id": self._id,
            "client_id": self.client_id,
            "type_commande": self.type_commande,
            "frais_livraison": self.frais_livraison,
            "produits": self.produits,
            "date_commande": self.date_commande,
            "statut": self.statut,
            "total": self.calculer_total()
        }
