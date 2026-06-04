from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, Response
from app import db
from app.models.product import Product, Category
from app.models.inquiry import Inquiry
import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).limit(3).all()
    categories = Category.query.all()
    return render_template('index.html', featured_products=featured_products, categories=categories)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        product_id = request.form.get('product_id') # optional, in case of product inquiry

        # Basic validation
        if not name or not email or not phone or not message:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for('main.contact'))

        try:
            # Create Inquiry record
            inquiry = Inquiry(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                product_id=int(product_id) if product_id else None
            )
            db.session.add(inquiry)
            db.session.commit()
            
            # Print in logs for lead awareness
            current_app.logger.info(f"New Lead Captured: Name: {name}, Email: {email}, Message: {message}")
            
            flash("Thank you! Your inquiry has been sent successfully. Our concierge will contact you shortly.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Inquiry error: {e}")
            flash("An error occurred. Please try again or contact us via WhatsApp.", "error")
            
        return redirect(url_for('main.contact'))

    return render_template('contact.html')

@main_bp.route('/gallery')
def gallery():
    products = Product.query.filter_by(is_active=True).all()
    categories = Category.query.all()
    return render_template('gallery.html', products=products, categories=categories)

@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main_bp.route('/terms')
def terms():
    return render_template('terms.html')

@main_bp.route('/robots.txt')
def robots():
    content = "User-agent: *\nAllow: /\nSitemap: " + url_for('main.sitemap', _external=True)
    return Response(content, mimetype="text/plain")

@main_bp.route('/sitemap.xml')
def sitemap():
    pages = []
    
    # Static pages
    ten_days_ago = (datetime.datetime.now() - datetime.timedelta(days=10)).date().isoformat()
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            # Exclude admin or API routes if any
            if not rule.rule.startswith('/api') and not rule.rule.startswith('/admin') and 'sitemap' not in rule.rule and 'robots' not in rule.rule:
                pages.append({
                    "loc": url_for(rule.endpoint, _external=True),
                    "lastmod": ten_days_ago
                })
                
    # Product pages
    products = Product.query.filter_by(is_active=True).all()
    for product in products:
        pages.append({
            "loc": url_for('products.detail', slug=product.slug, _external=True),
            "lastmod": product.created_at.date().isoformat() if product.created_at else ten_days_ago
        })
        
    sitemap_xml = render_template('sitemap_xml.html', pages=pages)
    return Response(sitemap_xml, mimetype="application/xml")
