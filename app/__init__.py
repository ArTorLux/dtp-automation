from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Ładujemy zmienne środowiskowe
load_dotenv()

# Tworzymy obiekt bazy danych (będzie używany w models.py)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Konfiguracja bazy danych
    database_url = os.getenv('DATABASE_URL', 'sqlite:///data/app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicjalizacja bazy
    db.init_app(app)
    Migrate(app, db)
    
    # CORS
    CORS(app)
    
    # Rejestrujemy trasy
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app
