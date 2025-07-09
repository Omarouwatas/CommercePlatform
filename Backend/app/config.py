import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-jwt-secret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/commerce_platform")
