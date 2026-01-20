from PIL import Image, ImageDraw
import os
import math

def create_glossy_image(filename, color_start, color_end):
    width, height = 1920, 1080
    image = Image.new('RGB', (width, height), color_start)
    draw = ImageDraw.Draw(image)
    
    # Draw Gradient Background
    for y in range(height):
        r = int(color_start[0] + (color_end[0] - color_start[0]) * y / height)
        g = int(color_start[1] + (color_end[1] - color_start[1]) * y / height)
        b = int(color_start[2] + (color_end[2] - color_start[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Add "Glossy" Reflections (Light streaks)
    # Diagonal white/transparent streaks
    for i in range(0, width + height, 400):
        # Draw a wide semi-transparent white line
        start_x = i
        start_y = 0
        end_x = i - height
        end_y = height
        
        # Manually drawing lines with varied transparency is hard in standard PIL without alpha composite
        # Simulating by drawing lighter lines
        draw.line([(start_x, start_y), (end_x, end_y)], fill=(255, 255, 255), width=2)
        draw.line([(start_x+50, start_y), (end_x+50, end_y)], fill=(200, 200, 200), width=10)
        draw.line([(start_x+100, start_y), (end_x+100, end_y)], fill=(150, 150, 150), width=5)

    # Save to app/static
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    static_dir = os.path.join(base_dir, 'app', 'static')
    
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    image.save(os.path.join(static_dir, filename))
    print(f"Created {filename}")

if __name__ == '__main__':
    # 1. Midnight Blue
    create_glossy_image('hero_glossy_1.png', (10, 10, 30), (20, 20, 80))
    # 2. Deep Red
    create_glossy_image('hero_glossy_2.png', (30, 0, 0), (80, 10, 10))
    # 3. Dark Gold
    create_glossy_image('hero_glossy_3.png', (30, 25, 5), (100, 80, 10))
