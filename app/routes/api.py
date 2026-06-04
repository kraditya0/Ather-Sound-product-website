from flask import Blueprint, jsonify, request
from app import db
from app.models.product import Product, Category
from app.models.inquiry import Inquiry

api_bp = Blueprint('api', __name__)

@api_bp.route('/products', methods=['GET'])
def get_products():
    category_slug = request.args.get('category')
    featured = request.args.get('featured')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
            
    if featured is not None:
        is_featured = featured.lower() in ['true', '1', 'yes']
        query = query.filter_by(is_featured=is_featured)
        
    products = query.all()
    return jsonify([p.to_dict() for p in products])

@api_bp.route('/products/<slug>', methods=['GET'])
def get_product(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@api_bp.route('/inquiry', methods=['POST'])
def create_inquiry():
    data = request.get_json() or {}
    
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    subject = data.get('subject')
    product_id = data.get('product_id')
    
    if not name or not email or not phone or not message:
        return jsonify({'error': 'Missing required fields (name, email, phone, message)'}), 400
        
    try:
        inquiry = Inquiry(
            name=name,
            email=email,
            phone=phone,
            message=message,
            subject=subject,
            product_id=product_id
        )
        db.session.add(inquiry)
        db.session.commit()
        return jsonify({'success': True, 'inquiry_id': inquiry.id}), 21
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
