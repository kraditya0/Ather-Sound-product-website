from app import db
from app.models.product import Category, Product

def seed_db():
    # Check if category table already has items
    if Category.query.first():
        print("Database already has categories. Skipping seed.")
        return False
        
    print("Seeding database...")
    
    # 1. Create Categories
    headphones_cat = Category(
        name="Headphones",
        slug="headphones",
        description="Premium over-ear acoustic models engineered for isolation and rich soundstages.",
        image_url="/static/images/category-headphones.webp"
    )
    
    earbuds_cat = Category(
        name="Earbuds",
        slug="earbuds",
        description="Sculpted in-ear monitors for exceptional fidelity and mobility.",
        image_url="/static/images/category-earbuds.webp"
    )
    
    home_sound_cat = Category(
        name="Home Sound",
        slug="home-sound",
        description="Spatial audio centerpieces designed to blend seamlessly with premium architecture.",
        image_url="/static/images/category-homesound.webp"
    )
    
    db.session.add_all([headphones_cat, earbuds_cat, home_sound_cat])
    db.session.commit()
    
    # 2. Create Products
    
    # Aether Aeon
    aeon = Product(
        category_id=headphones_cat.id,
        name="Aether Aeon Over-Ear Headphones",
        slug="aether-aeon",
        price=899.0,
        short_description="Wireless active noise cancelling headphones with custom-tuned beryllium drivers and premium leather finish.",
        primary_image="/static/images/products/aeon-main.webp",
        long_description="Engineered to deliver the purest acoustic experience, the Aether Aeon combines world-class active noise cancellation with hand-crafted comfort. Custom 40mm Beryllium drivers produce an expansive soundstage, capturing every nuance of your favorite recordings. Surrounded by lambskin earcups and a lightweight anodized aluminum band, the Aeon is a work of art for both your eyes and ears.",
        images=[
            "/static/images/products/aeon-main.webp",
            "/static/images/products/aeon-detail-1.webp",
            "/static/images/products/aeon-detail-2.webp",
            "/static/images/products/aeon-lifestyle.webp"
        ],
        specs={
            "Driver Type": "40mm Custom Beryllium",
            "Frequency Response": "10 Hz - 45,000 Hz",
            "Impedance": "32 Ohms",
            "Battery Life": "Up to 38 hours (ANC Active)",
            "Connectivity": "Bluetooth 5.3 aptX Adaptive, USB-C, 3.5mm Jack",
            "Weight": "290g",
            "Materials": "Anodized Aluminum, Lambskin Leather, Memory Foam"
        },
        video_url="/static/videos/aeon-preview.mp4",
        is_featured=True
    )
    
    # Aether Horizon
    horizon = Product(
        category_id=earbuds_cat.id,
        name="Aether Horizon Earbuds",
        slug="aether-horizon",
        price=349.0,
        short_description="Audiophile-grade true wireless earbuds with custom balanced armature drivers and ceramic details.",
        primary_image="/static/images/products/horizon-main.webp",
        long_description="Experience studio-quality sound in a pocket-sized masterpiece. The Aether Horizon earbuds feature hybrid dual-driver acoustics, providing sparkling highs and deep, rich bass. Encased in a polished ceramic body with a solid brass charging case, they are a statement of modern style and uncompromised audio engineering.",
        images=[
            "/static/images/products/horizon-main.webp",
            "/static/images/products/horizon-detail-1.webp",
            "/static/images/products/horizon-lifestyle.webp"
        ],
        specs={
            "Driver Type": "Hybrid Dual-Driver (Dynamic + Balanced Armature)",
            "Battery Life": "8 Hours (24 Hours with charging case)",
            "Charging": "Qi Wireless Charging, USB-C Fast Charge",
            "Water Resistance": "IPX5 Sweat and Water Resistant",
            "ANC": "Hybrid Active Noise Cancellation",
            "Materials": "Polished Bio-Ceramic, Hand-Finished Brass"
        },
        video_url="/static/videos/horizon-preview.mp4",
        is_featured=True
    )
    
    # Aether Monolith
    monolith = Product(
        category_id=home_sound_cat.id,
        name="Aether Monolith Soundbar",
        slug="aether-monolith",
        price=2499.0,
        short_description="Dolby Atmos-enabled architectural soundbar carved from a single block of Travertine stone and brushed aluminum.",
        primary_image="/static/images/products/monolith-main.webp",
        long_description="The Monolith is the centerpiece of the modern living space. It is a spatial audio home entertainment system that seamlessly blends sculpture and acoustic power. Carved from a solid piece of Travertine marble and aluminum, it houses 11 high-performance speakers that fill your entire room with immersive, high-resolution Dolby Atmos sound.",
        images=[
            "/static/images/products/monolith-main.webp",
            "/static/images/products/monolith-detail-1.webp",
            "/static/images/products/monolith-detail-2.webp",
            "/static/images/products/monolith-lifestyle.webp"
        ],
        specs={
            "Amplifiers": "11 Class D Amplifiers (total 650 Watts)",
            "Acoustics": "4x 4-inch Woofers, 4x 2-inch Midranges, 3x 1-inch Tweeters",
            "Spatial Audio": "Dolby Atmos 5.1.2 Spatial Decoding",
            "Streaming Services": "AirPlay 2, Chromecast, Spotify Connect, TIDAL Connect",
            "Inputs": "HDMI eARC, Optical In, Ethernet, Wi-Fi 6",
            "Dimensions": "110cm x 15cm x 12cm",
            "Materials": "Italian Travertine Stone, Anodized Aluminum, Premium Kvadrat Fabric"
        },
        video_url="/static/videos/monolith-preview.mp4",
        is_featured=True
    )
    
    # Aether Orbit
    orbit = Product(
        category_id=home_sound_cat.id,
        name="Aether Orbit Portable Speaker",
        slug="aether-orbit",
        price=599.0,
        short_description="Compact 360-degree wireless speaker with omnidirectional acoustic lenses and hand-sewn leather strap.",
        primary_image="/static/images/products/orbit-main.webp",
        long_description="Take luxury sound wherever you go. The Aether Orbit projects audio in a full 360-degree radius using a unique acoustic lens design. Crafted with a sandblasted aluminum chassis and a full-grain leather carry strap, it offers elegant portable sound that lasts all day and night.",
        images=[
            "/static/images/products/orbit-main.webp",
            "/static/images/products/orbit-detail-1.webp",
            "/static/images/products/orbit-lifestyle.webp"
        ],
        specs={
            "Drivers": "1x 3.5-inch Woofer, 2x 1.5-inch Full Range Drivers",
            "Frequency Range": "45 Hz - 22,000 Hz",
            "Battery Life": "Up to 24 Hours",
            "Water Resistance": "IP54 Dust and Splash Resistant",
            "Connectivity": "Bluetooth 5.2, Multipoint Stereo Pairing",
            "Weight": "1.2 kg",
            "Materials": "Sandblasted Aluminum, Full-Grain Leather, Polymer"
        },
        video_url="/static/videos/orbit-preview.mp4",
        is_featured=False
    )
    
    db.session.add_all([aeon, horizon, monolith, orbit])
    db.session.commit()
    print("Database successfully seeded.")
    return True
