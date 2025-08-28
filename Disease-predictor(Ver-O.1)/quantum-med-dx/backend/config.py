import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")
    API_KEY = os.getenv("API_KEY", "your_api_key")
    OTHER_CONFIG = os.getenv("OTHER_CONFIG", "default_value")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# You can add more configuration classes as needed (e.g., TestingConfig)