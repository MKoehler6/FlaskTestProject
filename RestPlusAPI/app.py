from flask import Flask, Blueprint
from RestPlusAPI import settings
from RestPlusAPI.api.myAPI import api
from RestPlusAPI.api.shop.endpoints.products import namespace as productsnamespace
from RestPlusAPI.database.db import db
from flask_cors import CORS # für den Zugriff von Vue von einem anderen Port


app = Flask(__name__)
CORS(app)


def configure_app(app):
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_EXPANSION # swagger: http://localhost:5000/api/
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VAL
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODS


def init_app(app):
    configure_app(app)
    blueprint = Blueprint('api', __name__, url_prefix='/api') # swagger: http://localhost:5000/api/
    api.init_app(blueprint)
    api.add_namespace(productsnamespace)
    app.register_blueprint(blueprint)
    db.init_app(app)


def main():
    init_app(app)
    app.run(debug=settings.FLASK_DEBUG, threaded=settings.FLASK_THREADED)


if __name__ == "__main__":
    main()