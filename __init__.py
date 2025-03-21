from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from redis import Redis
from config import config

mongo = PyMongo()
redis_client = Redis()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    mongo.init_app(app)
    
    # Initialize Redis
    global redis_client
    redis_client = Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'],
        decode_responses=True
    )
    
    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app