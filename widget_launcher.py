#!/usr/bin/env python3
"""
Sparky Desktop Widget Launcher
Run this to launch Sparky as a desktop widget on your homescreen
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from widget import run_widget_server
from dotenv import load_dotenv

load_dotenv()


def main():
    """Launch Sparky widget"""
    print("\n" + "=" * 70)
    print("🐞 SPARKY THE WEATHERBUG - DESKTOP WIDGET 🐞")
    print("=" * 70)
    print("\n✨ Features:")
    print("  🎤 Voice Activation - Say 'Hey Sparky!' or any weather question")
    print("  🟢🟡🔴 Dynamic Shell Color Alerts")
    print("  🌤️  Real-time Weather Data from WeatherBug")
    print("  💬 Interactive Responses")
    print("  🌐 Web-based Widget Interface")
    print("\n" + "=" * 70 + "\n")
    
    # Get API key from environment or arguments
    api_key = os.getenv("WEATHERBUG_API_KEY")
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    port = 5000
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            pass
    
    if not api_key and not os.getenv("OPENWEATHER_API_KEY"):
        print("⚠️  No API key found!")
        print("\nPlease set one of these environment variables:")
        print("  WEATHERBUG_API_KEY=your_key (Primary)")
        print("  OPENWEATHER_API_KEY=your_key (Fallback)")
        print("\nOr pass as argument:")
        print("  python widget_launcher.py YOUR_API_KEY")
        print("\nGet free API key at:")
        print("  WeatherBug: https://www.weatherbug.com/api")
        print("  OpenWeatherMap: https://openweathermap.org/api")
        sys.exit(1)
    
    print("🌐 Starting Widget Server on port", port)
    print("📱 Open browser to: http://localhost:" + str(port))
    print("🎤 Click the microphone button and ask 'What's the weather?'\n")
    
    run_widget_server(api_key=api_key, port=port, debug=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🐛 Sparky says: Stay safe! Widget shutting down... Goodbye! 🐛\n")
        sys.exit(0)
