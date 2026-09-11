# Sparky the Weatherbug - Configuration Guide

## Environment Variables

Create a `.env` file in the project root directory:

```bash
# OpenWeatherMap API Key (Required)
WEATHER_API_KEY=your_api_key_here
```

### Getting an API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to your API keys page
4. Copy your API key
5. Paste it into the `.env` file

## Customization

You can customize Sparky's behavior by editing `main.py`:

### Change Sparky's Personality

In the `SparkyWeatherAssistant.__init__` method:

```python
self.personality = [
    "Your custom message here! 🐛",
    "Another personality trait!",
]
```

### Adjust Danger Thresholds

In the `assess_danger_level` method:

```python
# Example: Change temperature threshold for red alert
if temp < -50:  # Changed from -40
    return AlertLevel.DANGER
```

### Modify Weather Icons

In the `WeatherIcon` enum:

```python
class WeatherIcon(Enum):
    CUSTOM_WEATHER = ("❄️", "Custom Description")
```

## Troubleshooting

### "Weather API key not found" Error

- Make sure you created a `.env` file in the project root
- Verify the environment variable is named `WEATHER_API_KEY`
- Check that your API key is valid

### "Failed to fetch weather data" Error

- Verify your internet connection
- Check if the city name is spelled correctly
- Ensure your API key is active (check OpenWeatherMap dashboard)
- Rate limiting: If making many requests, wait a moment before trying again

### Speech bubbles not displaying correctly

- Ensure your terminal supports Unicode characters
- Try using a modern terminal emulator (Windows Terminal, iTerm2, etc.)

## Running Sparky in Different Environments

### Windows

```bash
python main.py
```

### macOS/Linux

```bash
python3 main.py
```

### Docker (Coming Soon)

```bash
docker build -t sparky-weatherbug .
docker run -e WEATHER_API_KEY=your_key sparky-weatherbug
```

## API Rate Limits

OpenWeatherMap free tier allows:
- 60 calls/minute
- 1,000,000 calls/month

Sparky respects these limits by default!
