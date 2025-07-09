from bson import ObjectId
from datetime import datetime

class Product:
    def __init__(self, nom, prix, quantite, description="", categorie="", _id=None, date_ajout=None):
        self._id = _id if _id else ObjectId()
        self.nom = nom
        self.prix = float(prix)
        self.quantite = int(quantite)
        self.description = description
        self.categorie = categorie
        self.date_ajout = date_ajout if date_ajout else datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "nom": self.nom,
            "prix": self.prix,
            "quantite": self.quantite,
            "description": self.description,
            "categorie": self.categorie,
            "date_ajout": self.date_ajout
        }

    @staticmethod
    def from_dict(data):
        return Product(
            nom=data.get("nom"),
            prix=data.get("prix"),
            quantite=data.get("quantite"),
            description=data.get("description", ""),
            categorie=data.get("categorie", ""),
            _id=data.get("_id"),
            date_ajout=data.get("date_ajout")
        )
