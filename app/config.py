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
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '919876543210') # Default fallback (e.g., country code + number)
    WHATSAPP_DEFAULT_MESSAGE = "Hello, I am interested in the {product_name}. Please provide more information."
    
    # Contact Info
    CONTACT_PHONE = os.environ.get('CONTACT_PHONE', '+1 (800) 555-0199')
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'concierge@aetheraudio.com')
    CONTACT_ADDRESS = os.environ.get('CONTACT_ADDRESS', '742 Acoustic Boulevard, Sound District, NY 10001')
    CONTACT_HOURS = "Monday - Saturday: 10:00 AM - 8:00 PM | Sunday: Closed"
    MAPS_EMBED_URL = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.417240059345!2d-73.98744468459379!3d40.75889497932681!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25859a1c54b3b%3A0xe7c87c0ffbe4c1e4!2sTimes%20Square!5e0!3m2!1sen!2sus!4v1620000000000!5m2!1sen!2sus"
    
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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
