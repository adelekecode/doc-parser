import os
from datetime import timedelta

class Config:




    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/pitch-deck-uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    ALLOWED_EXTENSIONS = {'pdf', 'pptx'}
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/pitch_deck_parser')
    
    # Redis Configuration
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    
    # RabbitMQ Configuration
    RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
    RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'guest')
    RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', 'guest')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.environ.get('TEST_MONGO_URI', 'mongodb://localhost:27017/pitch_deck_parser_test')

class ProductionConfig(Config):
    DEBUG = False
    # In production, ensure all configuration is loaded from environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    



    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}