import json
from datetime import datetime
from app import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    
    products = db.relationship('Product', backref='category', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, slug, description=None, image_url=None):
        self.name = name
        self.slug = slug
        self.description = description
        self.image_url = image_url

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    short_description = db.Column(db.String(255), nullable=False)
    long_description = db.Column(db.Text, nullable=True)
    primary_image = db.Column(db.String(255), nullable=False)
    
    # Store images and specs as JSON strings to maintain cross-database compatibility (SQLite, PostgreSQL, MySQL)
    _images = db.Column('images', db.Text, nullable=True)
    _specs = db.Column('specs', db.Text, nullable=True)
    
    video_url = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, category_id, name, slug, price, short_description, primary_image, 
                 long_description=None, images=None, specs=None, video_url=None, 
                 is_featured=False, is_active=True):
        self.category_id = category_id
        self.name = name
        self.slug = slug
        self.price = price
        self.short_description = short_description
        self.primary_image = primary_image
        self.long_description = long_description
        self.images = images or []
        self.specs = specs or {}
        self.video_url = video_url
        self.is_featured = is_featured
        self.is_active = is_active

    @property
    def images(self):
        if not self._images:
            return []
        try:
            return json.loads(self._images)
        except Exception:
            return []

    @images.setter
    def images(self, value):
        self._images = json.dumps(value or [])

    @property
    def specs(self):
        if not self._specs:
            return {}
        try:
            return json.loads(self._specs)
        except Exception:
            return {}

    @specs.setter
    def specs(self, value):
        self._specs = json.dumps(value or {})

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'name': self.name,
            'slug': self.slug,
            'price': self.price,
            'short_description': self.short_description,
            'long_description': self.long_description,
            'primary_image': self.primary_image,
            'images': self.images,
            'specs': self.specs,
            'video_url': self.video_url,
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
