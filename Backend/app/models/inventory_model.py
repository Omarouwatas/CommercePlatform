from bson import ObjectId
from datetime import datetime

class Inventory:
    def __init__(self, product_id, quantite_disponible, emplacement, _id=None):
        self._id = _id if _id else ObjectId()
        self.product_id = product_id
        self.quantite_disponible = int(quantite_disponible)
        self.emplacement = emplacement
        self.date_ajout = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "product_id": self.product_id,
            "quantite_disponible": self.quantite_disponible,
            "emplacement": self.emplacement,
            "date_ajout": self.date_ajout
        }

    @staticmethod
    def from_dict(data):
        return Inventory(
            product_id=data.get("product_id"),
            quantite_disponible=data.get("quantite_disponible"),
            emplacement=data.get("emplacement"),
            _id=data.get("_id")
        )
