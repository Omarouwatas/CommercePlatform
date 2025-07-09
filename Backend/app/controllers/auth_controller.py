# auth_controller.py
from app.models.user_model import User
from app.extensions import mongo

user = User(email=data["email"], password=hashed_password)
mongo.db.users.insert_one(user.to_dict())
