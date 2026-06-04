import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# Look for a .env file in the root workspace directory
load_dotenv(os.path.join(basedir, '..', '.env'), override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aether-secret-luxury-key-9982481')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Brand Customization (Content Management)
    BRAND_NAME = "AETHER"
    BRAND_TAGLINE = "Pure Acoustic Sculptures"
    
    # WhatsApp configuration
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '+918766382326') # Default fallback (e.g., country code + number)
    WHATSAPP_DEFAULT_MESSAGE = "Hello, I am interested in the {product_name}. Please provide more information."
    
    # Contact Info
    CONTACT_PHONE = os.environ.get('CONTACT_PHONE', '+918766382326')
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'adityaiitm27@gmail.com')
    CONTACT_ADDRESS = os.environ.get('CONTACT_ADDRESS', 'sector 63 Noida, Electronic city, UP 201301')
    CONTACT_HOURS = "Monday - Saturday: 10:00 AM - 8:00 PM | Sunday: Closed"
    MAPS_EMBED_URL = os.environ.get('MAPS_EMBED_URL', 'https://maps.google.com/maps?q=noida%20electronic%20city&z=14&output=embed')
    
    # Social Media Configs
    SOCIAL_LINKS = {
        'instagram': 'https://instagram.com/aetheraudio',
        'facebook': 'https://facebook.com/aetheraudio',
        'youtube': 'https://youtube.com/aetheraudio',
        'linkedin': 'https://linkedin.com/company/aetheraudio',
        'twitter': 'https://twitter.com/aetheraudio'
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, '..', 'instance', 'app.db')}")

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, '..', 'instance', 'app.db')}")

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
