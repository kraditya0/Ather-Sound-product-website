import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config_by_name

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Ensure the instance folder exists (for SQLite)
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Register template filters
    @app.template_filter('currency')
    def currency_filter(value):
        try:
            return f"${float(value):,.2f}"
        except (ValueError, TypeError):
            return value

    # Context processor to make brand configs globally accessible in templates
    @app.context_processor
    def inject_brand_config():
        import datetime
        return {
            'brand_name': app.config['BRAND_NAME'],
            'brand_tagline': app.config['BRAND_TAGLINE'],
            'whatsapp_number': app.config['WHATSAPP_NUMBER'],
            'whatsapp_template': app.config['WHATSAPP_DEFAULT_MESSAGE'],
            'contact_phone': app.config['CONTACT_PHONE'],
            'contact_email': app.config['CONTACT_EMAIL'],
            'contact_address': app.config['CONTACT_ADDRESS'],
            'contact_hours': app.config['CONTACT_HOURS'],
            'maps_embed_url': app.config['MAPS_EMBED_URL'],
            'social_links': app.config['SOCIAL_LINKS'],
            'datetime': datetime
        }

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app
