from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

mongo = PyMongo()
jwt = JWTManager()
