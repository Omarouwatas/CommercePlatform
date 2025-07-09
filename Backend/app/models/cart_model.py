from bson import ObjectId
from datetime import datetime

class ElementPanier:
    def __init__(self, product_id, quantite):
        self.product_id = product_id
        self.quantite = int(quantite)

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantite": self.quantite
        }

class Panier:
    def __init__(self, utilisateur_id, elements=None, date_creation=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.utilisateur_id = utilisateur_id
        self.elements = elements if elements else []
        self.date_creation = date_creation if date_creation else datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "utilisateur_id": self.utilisateur_id,
            "elements": [e.to_dict() for e in self.elements],
            "date_creation": self.date_creation
        }

    @staticmethod
    def from_dict(data):
        elements = [ElementPanier(e["product_id"], e["quantite"]) for e in data.get("elements", [])]
        return Panier(
            utilisateur_id=data["utilisateur_id"],
            elements=elements,
            date_creation=data.get("date_creation"),
            _id=data.get("_id")
        )
