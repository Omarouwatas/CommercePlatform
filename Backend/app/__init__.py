from flask import Flask
from .extensions import mongo, jwt
from .routes.auth_routes import auth_bp
from .routes.products_routes import products_bp 
from app.routes.inventory_routes import inventory_bp
from app.routes.cart_routes import cart_bp
from app.routes.orders_routes import orders_bp

import app
def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    mongo.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")

    @app.route("/", methods=["GET"])
    def index():
        return {"msg": "Bienvenue sur l'API de gestion commerciale"}, 200
    return app

