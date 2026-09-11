# WIDGET_SETUP.md

# Sparky Desktop Widget Setup Guide

## What is Sparky Widget?

Sparky is a **desktop weather widget** that you can install on your desktop or homescreen. It features:

- 🎤 **Voice Activation** - Say "Hey Sparky!" or ask weather questions
- 🟢🟡🔴 **Dynamic Shell Color Alerts** - Real-time danger levels
- 🌤️ **Real-time Data** - Powered by WeatherBug API
- 💬 **Interactive Responses** - Friendly, personalized weather info
- 🌐 **Web-based** - Works in any modern browser

## Prerequisites

- Python 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- WeatherBug API key (free) or OpenWeatherMap API key (free)
- Microphone for voice activation

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a WeatherBug API Key (Recommended)

WeatherBug offers free API access:

1. Visit: https://www.weatherbug.com/api
2. Sign up for a free account
3. Create an API key
4. Copy your API key

### 3. Alternative: Get OpenWeatherMap API Key

If WeatherBug is not available:

1. Visit: https://openweathermap.org/api
2. Sign up for free
3. Get your API key from the dashboard
4. Copy your API key

### 4. Configure Environment

Create a `.env` file in your project directory:

```bash
# WeatherBug API (Recommended)
WEATHERBUG_API_KEY=your_weatherbug_key_here

# OR OpenWeatherMap API (Fallback)
OPENWEATHER_API_KEY=your_openweather_key_here
```

## Running the Widget

### Method 1: Simple Launch

```bash
python widget_launcher.py
```

Then open your browser to: **http://localhost:5000**

### Method 2: Custom Port

```bash
python widget_launcher.py <your_api_key> 8080
```

Opens at: **http://localhost:8080**

### Method 3: Direct Python

```bash
from widget import run_widget_server

run_widget_server(port=5000)
```

## Using the Widget

### Voice Activation

1. **Click the microphone button** 🎤
2. Say your weather question:
   - "What's the weather?"
   - "Is it raining in New York?"
   - "Weather in London"
   - "Check the forecast"
   - "How hot is it?"

3. Sparky responds with:
   - Weather icon (🐞)
   - Shell color alert (🟢🟡🔴)
   - Real-time conditions
   - Location info

### Text Input

Alternatively, type your question in the text field and press Enter or click the microphone button.

## Widget Features

### Shell Color System

- 🟢 **Green** - All clear, safe conditions
- 🟡 **Yellow** - Warning, severe weather approaching
- 🔴 **Red** - DANGER, seek shelter immediately!

### Weather Data

The widget displays:
- Current temperature (°C)
- "Feels like" temperature
- Weather description
- Humidity percentage
- Wind speed
- API source (WeatherBug or OpenWeatherMap)

### Voice Recognition

The widget uses Web Speech API for voice input:
- **Chrome/Edge** - Full support
- **Firefox** - Full support with flag enabled
- **Safari** - Limited support
- **Mobile** - Supported on most devices

## Desktop Installation (Windows/Mac/Linux)

### Windows Desktop Shortcut

1. Create a batch file `sparky_widget.bat`:

```batch
@echo off
python widget_launcher.py
pause
```

2. Right-click → Properties
3. Under "Shortcut" tab, change "Start in" to your project directory
4. Pin to taskbar or desktop

### macOS

Create `sparky_widget.command`:

```bash
#!/bin/bash
cd /path/to/sparky-weatherbug-assistant
python3 widget_launcher.py
```

Make executable:
```bash
chmod +x sparky_widget.command
```

### Linux

Create `sparky_widget.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Sparky Widget
Exec=python3 /path/to/widget_launcher.py
Icon=weather
Terminal=true
Categories=Utility;Weather;
```

## Browser Widget Installation

### Chrome Web App (Windows/Mac/Linux)

1. Open http://localhost:5000
2. Click menu (⋮) → "Install app"
3. Pin to taskbar

### Firefox

1. Open http://localhost:5000
2. Click menu (≡) → "Create Application Menu"
3. Customize and save

## Troubleshooting

### "No API key found" Error

Make sure your `.env` file is in the project root directory:

```bash
cat .env  # Check content
```

Should show:
```
WEATHERBUG_API_KEY=abc123xyz
```

### Microphone Not Working

1. Check browser permissions - allow microphone access
2. Test microphone at: https://www.webrtc-experiment.com/speech/
3. Try a different browser
4. Ensure JavaScript is enabled

### Weather Data Not Loading

1. Verify internet connection
2. Check API key is valid and active
3. Try different location names
4. Check browser console for errors (F12)

### Port Already in Use

If port 5000 is busy, use a different port:

```bash
python widget_launcher.py <api_key> 8080
```

## Voice Query Examples

### Weather Conditions

- "What's the weather?"
- "Is it sunny today?"
- "How cold is it?"
- "Check if it's raining"

### Locations

- "Weather in New York"
- "What's the temperature in London?"
- "Is it hot in Miami?"
- "Forecast for Sydney"

### Specific Questions

- "How's the humidity?"
- "What's the wind speed?"
- "Is there a storm coming?"
- "Will it snow tomorrow?"

## API Sources

### WeatherBug (Recommended)

**Pros:**
- Hyper-local weather data
- Frequent updates
- Storm tracking
- Free tier available

**Cons:**
- Slightly limited forecast data

### OpenWeatherMap (Fallback)

**Pros:**
- 5-day forecast included
- Extensive data
- Free tier available

**Cons:**
- Less hyper-local

## Advanced Configuration

### Custom Location

Set default location in `.env`:

```bash
DEFAULT_LOCATION=San Francisco
```

### Disable Voice

To disable voice and use text-only:

Edit `widget.py` - comment out voice recognition code

### Custom Styling

Edit the CSS in `WIDGET_HTML` in `widget.py` to customize appearance

### Change Port Dynamically

```python
from widget import run_widget_server

run_widget_server(api_key="your_key", port=3000)
```

## Performance Tips

1. Use modern browser (Chrome/Edge recommended)
2. Run on machine with good internet connection
3. Keep browser window open for persistent widget
4. Refresh if responses become slow

## Security Notes

- API keys are stored locally in `.env`
- Never commit `.env` to version control
- The widget server runs locally (not exposed online)
- Voice data is processed client-side when possible

## Next Steps

1. ✅ Install dependencies
2. ✅ Get API key
3. ✅ Configure `.env`
4. ✅ Launch widget
5. ✅ Ask Sparky about the weather!

## Support

For issues:
1. Check this guide first
2. Review error messages in browser console (F12)
3. Check Python console output
4. Verify API key and internet connection

Enjoy your Sparky Widget! 🐞✨
