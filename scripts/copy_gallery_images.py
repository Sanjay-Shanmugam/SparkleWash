import shutil
import os

source_dir = r"C:\Users\Nivetha\.gemini\antigravity\brain\bdb23188-7e9a-43e1-9192-b400d93be7a7"
# Use relative path to app/static
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dest_dir = os.path.join(base_dir, 'app', 'static')

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

files = [
    ("uploaded_image_0_1768887854077.jpg", "gallery_defender.jpg"),
    ("uploaded_image_1_1768887854077.jpg", "gallery_audi.jpg"),
    ("uploaded_image_2_1768887854077.jpg", "gallery_black.jpg"),
    ("uploaded_image_3_1768887854077.jpg", "gallery_interior.jpg")
]

print("Copying gallery images...")
for src_name, dest_name in files:
    src_path = os.path.join(source_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    try:
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_name} -> {dest_name}")
        else:
            print(f"Source file not found: {src_name}")
    except Exception as e:
        print(f"Error copying {src_name}: {e}")

print("Done.")
