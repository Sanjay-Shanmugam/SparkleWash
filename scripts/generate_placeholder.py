from PIL import Image, ImageDraw
import os

def create_placeholder():
    # Create a 1920x1080 image
    width, height = 1920, 1080
    image = Image.new('RGB', (width, height), (5, 5, 5)) # Almost black
    draw = ImageDraw.Draw(image)
    
    # Draw a subtle gradient or lines
    for i in range(0, height, 10):
        color = int(20 - (i / height) * 20)
        draw.line([(0, i), (width, i)], fill=(color, color, color))
    
    # Save to app/static
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    static_dir = os.path.join(base_dir, 'app', 'static')

    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        
    image.save(os.path.join(static_dir, 'hero_1.png'))
    print("Placeholder hero_1.png created.")

if __name__ == '__main__':
    try:
        create_placeholder()
    except ImportError:
        print("PIL not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "pillow"])
        from PIL import Image, ImageDraw
        create_placeholder()
