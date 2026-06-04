from datetime import datetime
from app import db

class Inquiry(db.Model):
    __tablename__ = 'inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=True)
    message = db.Column(db.Text, nullable=False)
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Establish relationship to Product if specific inquiries are about a product
    product = db.relationship('Product', backref=db.backref('inquiries', lazy=True))

    def __init__(self, name, phone, email, message, subject=None, product_id=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.message = message
        self.subject = subject
        self.product_id = product_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
