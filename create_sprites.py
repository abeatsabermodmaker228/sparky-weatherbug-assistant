#!/usr/bin/env python3
"""
Sprite Animation Demo
Shows how to create and test sprite animations for Sparky
"""

from PIL import Image, ImageDraw
import os


def create_sample_sprite(filename: str, weather_type: str):
    """
    Create a sample sprite GIF for testing
    
    Args:
        filename: Output filename
        weather_type: Type of weather for the sprite
    """
    os.makedirs("sprites", exist_ok=True)
    
    # Create frames for animation
    frames = []
    colors = {
        "clear_day": [(255, 200, 0), (100, 150, 255)],  # Yellow/blue
        "clear_night": [(50, 50, 100), (200, 200, 255)],  # Dark blue/light blue
        "cloudy": [(150, 150, 150), (200, 200, 200)],  # Gray tones
        "rainy": [(50, 50, 100), (100, 150, 200)],  # Dark blue/light blue
        "thunderstorm": [(80, 0, 100), (255, 255, 0)],  # Purple/yellow
        "snow": [(200, 200, 255), (255, 255, 255)],  # Light blue/white
        "foggy": [(180, 180, 180), (220, 220, 220)],  # Gray
        "windy": [(100, 100, 200), (150, 200, 255)],  # Blue tones
        "hail": [(100, 100, 150), (200, 200, 220)],  # Blue-gray
        "tornado": [(80, 80, 80), (255, 0, 0)],  # Dark gray/red
    }
    
    bg_color, accent_color = colors.get(weather_type, [(100, 100, 100), (200, 200, 200)])
    
    # Create 8 frames for animation
    for frame_num in range(8):
        # Create image
        img = Image.new("RGB", (200, 200), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw simple Sparky bug shape (circle body)
        offset = 5 * (frame_num % 2)  # Slight bounce
        center_x = 100 + offset
        center_y = 100 + offset
        
        # Body (circle)
        draw.ellipse(
            [center_x - 40, center_y - 40, center_x + 40, center_y + 40],
            fill=accent_color,
            outline=(0, 0, 0),
            width=2
        )
        
        # Eyes
        draw.ellipse([center_x - 20, center_y - 15, center_x - 10, center_y - 5], fill=(0, 0, 0))
        draw.ellipse([center_x + 10, center_y - 15, center_x + 20, center_y - 5], fill=(0, 0, 0))
        
        # Mouth
        draw.arc([center_x - 15, center_y, center_x + 15, center_y + 20], 0, 180, fill=(0, 0, 0), width=2)
        
        # Antennae
        draw.line([center_x, center_y - 40, center_x - 15, center_y - 60], fill=(0, 0, 0), width=2)
        draw.line([center_x, center_y - 40, center_x + 15, center_y - 60], fill=(0, 0, 0), width=2)
        
        # Add weather-specific elements
        if weather_type == "rainy":
            # Draw raindrops
            for i in range(3):
                y = 50 + (i * 40) + (frame_num * 10)
                draw.line([center_x + 60, y, center_x + 60, y + 10], fill=(100, 150, 255), width=2)
        
        elif weather_type == "thunderstorm":
            # Draw lightning
            draw.polygon([
                (center_x + 50, center_y - 50),
                (center_x + 60, center_y - 30),
                (center_x + 55, center_y - 20),
                (center_x + 70, center_y),
            ], fill=(255, 255, 0), outline=(255, 200, 0), width=2)
        
        elif weather_type == "snow":
            # Draw snowflakes
            for i in range(3):
                x = 50 + (i * 50)
                y = 50 + (frame_num * 5)
                draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 255, 255))
        
        elif weather_type == "windy":
            # Draw wind lines
            for i in range(3):
                y = 50 + (i * 40)
                x_offset = (frame_num * 15) % 60
                draw.line(
                    [center_x + 60 - x_offset, y, center_x + 80 - x_offset, y],
                    fill=(150, 150, 200),
                    width=3
                )
        
        frames.append(img)
    
    # Save as animated GIF
    frames[0].save(
        os.path.join("sprites", filename),
        save_all=True,
        append_images=frames[1:],
        duration=150,  # 150ms per frame
        loop=0  # Loop forever
    )
    
    print(f"✅ Created: sprites/{filename}")


def create_all_sample_sprites():
    """Create all sample sprite GIFs"""
    print("🐞 Creating sample Sparky sprites...")
    print()
    
    sprites = {
        "sparky_clear_day.gif": "clear_day",
        "sparky_clear_night.gif": "clear_night",
        "sparky_cloudy.gif": "cloudy",
        "sparky_rainy.gif": "rainy",
        "sparky_thunderstorm.gif": "thunderstorm",
        "sparky_snow.gif": "snow",
        "sparky_foggy.gif": "foggy",
        "sparky_windy.gif": "windy",
        "sparky_hail.gif": "hail",
        "sparky_tornado.gif": "tornado",
    }
    
    for filename, weather_type in sprites.items():
        create_sample_sprite(filename, weather_type)
    
    print()
    print("=" * 60)
    print("✅ All sample sprites created in 'sprites/' directory!")
    print("=" * 60)
    print()
    print("You can now run: python main.py")
    print()
    print("💡 Tip: Replace these sample sprites with actual artwork")
    print("   from the BETA version or your own custom designs!")
    print()


if __name__ == "__main__":
    create_all_sample_sprites()
