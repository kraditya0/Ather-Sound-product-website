import unittest
from app import create_app, db
from app.models.product import Product, Category
from app.models.inquiry import Inquiry

class AetherAppTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        # Initialize db tables in memory
        with self.app.app_context():
            db.create_all()
            
            # Seed test categories and products
            cat = Category(name="Test Category", slug="test-cat", description="A test category")
            db.session.add(cat)
            db.session.commit()
            
            prod = Product(
                category_id=cat.id,
                name="Test Headphone",
                slug="test-headphone",
                price=500.0,
                short_description="A test headphone",
                primary_image="/static/images/test.webp",
                long_description="A test headphone details",
                specs={"Driver": "40mm"}
            )
            db.session.add(prod)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_homepage_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Acoustic sculptures', response.data)

    def test_products_route(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Headphone', response.data)

    def test_product_detail_route(self):
        response = self.client.get('/products/test-headphone')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Headphone', response.data)
        self.assertIn(b'$500.00', response.data)

    def test_product_detail_not_found(self):
        response = self.client.get('/products/non-existent-product')
        self.assertEqual(response.status_code, 404)

    def test_about_route(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Heritage', response.data)

    def test_gallery_route(self):
        response = self.client.get('/gallery')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Portfolio', response.data)

    def test_contact_route_get(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bespoke Inquiry', response.data)

    def test_contact_inquiry_submission(self):
        response = self.client.post('/contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'subject': 'General Inquiry',
            'message': 'This is a test message'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'inquiry has been sent successfully', response.data)
        
        # Verify db insert
        with self.app.app_context():
            inquiry = Inquiry.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(inquiry)
            self.assertEqual(inquiry.name, 'Test User')
            self.assertEqual(inquiry.message, 'This is a test message')

    def test_api_products(self):
        response = self.client.get('/api/v1/products')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['slug'], 'test-headphone')

    def test_api_categories(self):
        response = self.client.get('/api/v1/categories')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['slug'], 'test-cat')

    def test_sitemap_xml(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/xml')
        self.assertIn(b'<loc>', response.data)
        self.assertIn(b'test-headphone', response.data)

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/plain')
        self.assertIn(b'User-agent: *', response.data)

if __name__ == '__main__':
    unittest.main()
