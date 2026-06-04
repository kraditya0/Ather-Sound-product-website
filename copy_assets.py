import os
import shutil
import glob

# Setup destination path
dest_dir = "/home/aditya/Documents/WebApp/app/static/images/products"
os.makedirs(dest_dir, exist_ok=True)

# Find generated files in brain folder
brain_dir = "/home/aditya/.gemini/antigravity/brain/9ff21ba8-129c-4c70-83b4-336c3f87dbeb"

mappings = {
    'aeon_main': ['aeon-main.webp', 'aeon-detail-1.webp', 'aeon-detail-2.webp', 'aeon-lifestyle.webp'],
    'horizon_main': ['horizon-main.webp', 'horizon-detail-1.webp', 'horizon-lifestyle.webp'],
    'monolith_main': ['monolith-main.webp', 'monolith-detail-1.webp', 'monolith-detail-2.webp', 'monolith-lifestyle.webp'],
    'orbit_main': ['orbit-main.webp', 'orbit-detail-1.webp', 'orbit-lifestyle.webp']
}

for prefix, target_filenames in mappings.items():
    # Search for files starting with prefix in brain_dir
    files = glob.glob(os.path.join(brain_dir, f"{prefix}_*.png"))
    if not files:
        print(f"No files found for {prefix}")
        continue
    
    # Get the latest generated file for this prefix
    latest_file = max(files, key=os.path.getctime)
    print(f"Latest file for {prefix}: {latest_file}")
    
    for filename in target_filenames:
        target_path = os.path.join(dest_dir, filename)
        shutil.copy2(latest_file, target_path)
        print(f"Copied to {target_path}")

print("Assets copying complete.")
