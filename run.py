import os
from app import create_app, db
from app.services.db_init import seed_db

config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

# Auto-initialize database tables and seed with data on startup
with app.app_context():
    db.create_all()
    seed_db()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
