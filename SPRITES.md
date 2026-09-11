# Sparky the Weatherbug - Sprite Setup Guide

## Using Custom Sprite GIFs

Sparky now supports custom sprite animations! You can use sprites from the BETA version or create your own.

## Directory Structure

```
sparky-weatherbug-assistant/
├── main.py
├── requirements.txt
├── sprites/
│   ├── sparky_clear_day.gif
│   ├── sparky_clear_night.gif
│   ├── sparky_cloudy.gif
│   ├── sparky_rainy.gif
│   ├── sparky_thunderstorm.gif
│   ├── sparky_snow.gif
│   ├── sparky_foggy.gif
│   ├── sparky_windy.gif
│   ├── sparky_hail.gif
│   └── sparky_tornado.gif
└── .env
```

## Sprite Files Needed

Create a `sprites/` directory in the project root and add these GIF files:

| Sprite File | Weather Condition | Description |
|-------------|------------------|-------------|
| `sparky_clear_day.gif` | Clear/Sunny | Sparky happy and glowing ☀️ |
| `sparky_clear_night.gif` | Clear Night | Sparky with moon 🌙 |
| `sparky_cloudy.gif` | Cloudy | Sparky with clouds ⛅ |
| `sparky_rainy.gif` | Rainy | Sparky with rain animation 🌧️ |
| `sparky_thunderstorm.gif` | Thunderstorm | Sparky with lightning ⛈️ |
| `sparky_snow.gif` | Snow | Sparky with snow animation ❄️ |
| `sparky_foggy.gif` | Foggy/Misty | Sparky in fog 🌫️ |
| `sparky_windy.gif` | Windy | Sparky blown by wind 💨 |
| `sparky_hail.gif` | Hail | Sparky with hail 🌨️ |
| `sparky_tornado.gif` | Tornado/Hurricane | Sparky in danger! 🌪️ |

## Getting BETA Sprites

If you have sprites from the original Sparky BETA app:

1. Extract sprite assets from the BETA version
2. Convert them to GIF format if needed
3. Place them in the `sprites/` directory
4. Rename them to match the expected filenames above

## Creating Custom Sprites

### Using Existing Images

```bash
from PIL import Image

# Convert PNG to GIF
img = Image.open("sparky_clear.png")
img.save("sprites/sparky_clear_day.gif")
```

### Creating Animated GIFs

```python
from PIL import Image

# Create animation from multiple frames
frames = [Image.open(f"frame_{i}.png") for i in range(10)]
frames[0].save(
    "sprites/sparky_clear_day.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,  # 100ms per frame
    loop=0  # Loop forever
)
```

## Sprite Requirements

- **Format**: GIF (supports animation), PNG, or JPG
- **Size**: Recommended 200x200 to 400x400 pixels
- **Colors**: Use Sparky's original color palette
- **Animation**: GIFs should be 8-12 frames for smooth animation

## Disabling Sprites

To run without sprites (ASCII mode):

```python
sparky = SparkyWeatherAssistant(use_sprites=False)
```

## Advanced Configuration

### Custom Sprite Directory

```python
sparky = SparkyWeatherAssistant(
    use_sprites=True,
    custom_sprite_dir="my_custom_sprites"
)
```

### Adding New Weather Types

Edit `WeatherSprite` enum in `main.py`:

```python
class WeatherSprite(Enum):
    MY_CUSTOM_WEATHER = "sprites/sparky_custom.gif"
```

Then update `get_sprite_path()` method to use it.

## Troubleshooting Sprites

### "Sprite file not found" Error

- Verify the `sprites/` directory exists
- Check sprite filenames match exactly (case-sensitive on Linux/Mac)
- Ensure file extensions are correct (.gif, .png, etc.)

### Sprite Not Displaying

- GIF might be corrupted - try opening in an image viewer
- Terminal might not support image display - try a modern terminal
- Use Pillow 10.0.0 or newer: `pip install --upgrade Pillow`

### Animation Too Fast/Slow

Edit the GIF duration in the source image editor or regenerate:

```python
img.save("sprites/sparky.gif", duration=150)  # 150ms per frame
```

## Web/GUI Implementation

For a web or GUI application, you can display sprites more dynamically:

```python
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
gif = Image.open("sprites/sparky_clear_day.gif")
photo = ImageTk.PhotoImage(gif)
label = tk.Label(root, image=photo)
label.pack()
root.mainloop()
```

## Next Steps

1. Create the `sprites/` directory
2. Add your custom sprite GIFs
3. Run `python main.py`
4. Sparky will now display animated sprites based on weather conditions!
