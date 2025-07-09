# user_model.py
from bson import ObjectId
from datetime import datetime


class User:
    def __init__(self, nom, email, mot_de_passe, role="client", adresse="", telephone="", _id=None, date_inscription=None):
        self._id = _id if _id else ObjectId()
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.role = role
        self.adresse = adresse
        self.telephone = telephone
        self.date_inscription = date_inscription if date_inscription else datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "nom": self.nom,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe,
            "role": self.role,
            "adresse": self.adresse,
            "telephone": self.telephone,
            "date_inscription": self.date_inscription
        }

    @staticmethod
    def from_dict(data):
        return User(
            nom=data.get("nom"),
            email=data.get("email"),
            mot_de_passe=data.get("mot_de_passe"),
            role=data.get("role", "client"),
            adresse=data.get("adresse", ""),
            telephone=data.get("telephone", ""),
            _id=data.get("_id"),
            date_inscription=data.get("date_inscription")
        )
