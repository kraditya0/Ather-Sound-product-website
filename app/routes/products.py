from flask import Blueprint, render_template, request, abort
from app.models.product import Product, Category

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def index():
    # Retrieve query params
    category_slug = request.args.get('category')
    search_query = request.args.get('q')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'featured')

    query = Product.query.filter_by(is_active=True)

    # 1. Category Filter
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)

    # 2. Search Filter
    if search_query:
        query = query.filter(
            (Product.name.ilike(f"%{search_query}%")) | 
            (Product.short_description.ilike(f"%{search_query}%")) |
            (Product.long_description.ilike(f"%{search_query}%"))
        )

    # 3. Price Filter
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # 4. Sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:  # 'featured'
        query = query.order_by(Product.is_featured.desc(), Product.created_at.desc())

    products = query.all()
    categories = Category.query.all()

    return render_template(
        'products.html', 
        products=products, 
        categories=categories,
        selected_category=category_slug,
        search_query=search_query,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by
    )

@products_bp.route('/<slug>')
def detail(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    # Get related products (same category, excluding current product)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(3).all()
    
    return render_template(
        'product_detail.html', 
        product=product, 
        related_products=related_products
    )
