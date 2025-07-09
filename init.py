# Création du modèle Product dans product_model.py

import os

product_model_code = '''from bson import ObjectId
from datetime import datetime

class Product:
    def __init__(self, name, price, stock, _id=None, created_at=None):
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.created_at = created_at if created_at else datetime.utcnow()
        self._id = _id if _id else ObjectId()

    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        return Product(
            name=data.get("name"),
            price=data.get("price"),
            stock=data.get("stock"),
            _id=data.get("_id"),
            created_at=data.get("created_at")
        )
'''

product_model_path = "backend/app/models/product_model.py"
os.makedirs(os.path.dirname(product_model_path), exist_ok=True)
with open(product_model_path, "w") as f:
    f.write(product_model_code)
