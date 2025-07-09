from flask_jwt_extended import get_jwt_identity
from app.extensions import mongo
from bson import ObjectId

def get_current_user():
    user_id = get_jwt_identity()
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})
