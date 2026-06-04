# AETHER — Pure Acoustic Sculptures

AETHER is a premium, modern, mobile-first business product showcase and lead-generation platform built for a luxury audio brand. It displays architectural acoustics, custom configurations, and lets potential clients submit concierge inquiries via integrated forms and context-aware WhatsApp triggers. 

The architecture is built on a modular Flask backend and a clean, responsive styling layer (Tailwind CSS, GSAP animations, vanilla JS), allowing it to easily scale into a full-fledged e-commerce platform in the future.

---

## Key Features

- **Luxury User Interface**: Built with high-end, responsive aesthetics, modern typography, glassmorphic navigations, custom interactive cursors, and fluid 60fps micro-animations.
- **Dynamic Product Catalog**: Browse collections (Headphones, Earbuds, Home Sound) with instant filtering, real-time search, and interactive spec accordions.
- **Product Detail Features**: Implements an interactive image gallery, hover image coordinate magnifier (zoom lens), and video lightbox modals.
- **Lead Generation Concierge**: A custom direct-inquiry submission form that captures leads, logs request history, and redirects to secure WhatsApp links with context-aware product messages.
- **Responsive Architecture**: Fully mobile-first design, adaptive masonry gallery structures, and layout filters.
- **Core SEO Integration**: Native JSON-LD structured schema metadata, Open Graph attributes, custom search engine indexing, and dynamic sitemaps (/sitemap.xml).
- **Dark/Light Mode**: Smooth theme toggling that respects browser defaults and stores preferences in localStorage.

---

## Tech Stack

- **Backend**: Flask (Python 3.10+)
- **Database**: SQLite (SQLAlchemy ORM)
- **Migrations**: Flask-Migrate (Alembic)
- **Frontend**: Tailwind CSS (Play CDN), GSAP (GreenSock Animation Platform), vanilla JS
- **Production Server**: Gunicorn

---

## Directory Structure

```text
├── app/
│   ├── config.py           # Configuration mapping (reads environment variables)
│   ├── __init__.py         # Application Factory, global jinja contexts, filters
│   ├── models/             # SQLAlchemy DB schemas
│   │   ├── product.py
│   │   └── inquiry.py
│   ├── routes/             # Blueprint routes (main, products, REST API v1)
│   │   ├── main.py
│   │   ├── products.py
│   │   └── api.py
│   ├── services/
│   │   └── db_init.py      # Database seed service (adds signature products)
│   ├── static/             # Static files (CSS, JS, assets)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/          # Jinja2 HTML templates
├── instance/               # SQLite database storage (gitignored)
├── .env                    # System variables (gitignored)
├── .env.example            # Environment variables placeholder config
├── requirements.txt        # PIP dependencies
├── run.py                  # Entrypoint runner
└── test_app.py             # Unit tests suite
```

---

## Getting Started

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Set Up a Virtual Environment
```bash
# Clone the repository and navigate into the root directory
cd Ather-Sound-product-website

# Create virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database and Seed Data
When you run the app for the first time, Flask will automatically create the SQLite database in the `/instance` folder and seed it with signature acoustics (Aeon Headphones, Horizon Earbuds, Monolith Soundbar, Orbit Speaker).

### 5. Run the Application
```bash
# Start the local development server
python run.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## Running Tests
Run the automated unittest suite to verify backend routes, database models, and API configurations:
```bash
python -m unittest test_app.py
```

---

## Deployment on Render

This project is configured to deploy directly to **Render** using the free web service tier.

1. Create a **New Web Service** on Render and link your Git repository.
2. Select **Python** runtime.
3. Configure settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
4. Add the following **Environment Variables** in the Render Dashboard:
   - `FLASK_CONFIG` = `production`
   - `SECRET_KEY` = `(your-secret-key)`
   - Any custom contact details (`WHATSAPP_NUMBER`, `CONTACT_EMAIL`, etc.)
