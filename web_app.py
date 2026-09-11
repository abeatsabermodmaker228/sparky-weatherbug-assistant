#!/usr/bin/env python3
"""
Sparky the Weatherbug - Full Web App with PWA Support
Desktop widget, desktop app, and mobile web app
"""

import os
import requests
import json
from datetime import datetime
from enum import Enum
from dotenv import load_dotenv
from typing import Optional, Dict, Tuple
import threading
import webbrowser

load_dotenv()


class AlertLevel(Enum):
    """Alert levels for weather conditions"""
    SAFE = "🟢"
    WARNING = "🟡"
    DANGER = "🔴"


class SparkyWeatherAssistant:
    """Sparky the Weatherbug - AI Weather Assistant with WeatherBug API"""

    def __init__(self, api_key: str = None):
        """Initialize Sparky Weather Assistant"""
        self.weatherbug_key = api_key or os.getenv("WEATHERBUG_API_KEY")
        self.openweather_key = os.getenv("OPENWEATHER_API_KEY")
        
        self.use_weatherbug = bool(self.weatherbug_key)
        
        if not self.use_weatherbug and not self.openweather_key:
            raise ValueError("No API key found. Set WEATHERBUG_API_KEY or OPENWEATHER_API_KEY")

        self.weatherbug_url = "https://api.weatherbug.com/v2/weather"
        self.weatherbug_location_url = "https://api.weatherbug.com/v2/location"
        self.openweather_url = "https://api.openweathermap.org/data/2.5/weather"

        self.personality = [
            "Stay safe out there, buddy! 🐛",
            "Sparky here with your weather update! ☀️",
            "Let's check what Mother Nature is cooking up! 🌦️",
            "Your friendly weatherbug reporting for duty! 🐞",
        ]

        self.last_location = "London"

    def get_weather_from_weatherbug(self, location: str) -> dict:
        """Fetch weather from WeatherBug API"""
        try:
            location_response = requests.get(
                self.weatherbug_location_url,
                params={"query": location, "apiKey": self.weatherbug_key},
                timeout=5
            )
            location_response.raise_for_status()
            location_data = location_response.json()

            if not location_data or "locations" not in location_data or len(location_data["locations"]) == 0:
                return {"error": f"Location '{location}' not found"}

            loc = location_data["locations"][0]
            lat, lon = loc.get("latitude"), loc.get("longitude")
            city = loc.get("displayName", location)

            weather_response = requests.get(
                self.weatherbug_url,
                params={
                    "lat": lat,
                    "lon": lon,
                    "apiKey": self.weatherbug_key,
                    "units": "metric"
                },
                timeout=5
            )
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            return {
                "name": city,
                "sys": {"country": location_data.get("locations", [{}])[0].get("country", "")},
                "main": {
                    "temp": weather_data.get("temperature", 0),
                    "feels_like": weather_data.get("feelsLike", 0),
                    "humidity": weather_data.get("humidity", 0),
                    "pressure": weather_data.get("pressure", 0)
                },
                "weather": [{
                    "main": weather_data.get("conditions", "Unknown"),
                    "description": weather_data.get("conditions", "Unknown").lower(),
                    "icon": weather_data.get("icon", "01d"),
                    "id": weather_data.get("weatherType", 0)
                }],
                "wind": {
                    "speed": weather_data.get("windSpeed", 0),
                    "deg": weather_data.get("windDirection", 0)
                },
                "source": "weatherbug"
            }

        except Exception as e:
            return {"error": f"WeatherBug API error: {str(e)}"}

    def get_weather_from_openweather(self, city: str) -> dict:
        """Fallback: Get weather from OpenWeatherMap"""
        try:
            response = requests.get(
                self.openweather_url,
                params={"q": city, "appid": self.openweather_key, "units": "metric"},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            data["source"] = "openweathermap"
            return data
        except Exception as e:
            return {"error": f"OpenWeatherMap API error: {str(e)}"}

    def get_weather(self, location: str) -> dict:
        """Get weather from WeatherBug or fallback"""
        self.last_location = location
        
        if self.use_weatherbug:
            data = self.get_weather_from_weatherbug(location)
            if "error" not in data:
                return data

        return self.get_weather_from_openweather(location)

    def assess_danger_level(self, weather_data: dict) -> AlertLevel:
        """Assess danger level"""
        if "error" in weather_data:
            return AlertLevel.SAFE

        main = weather_data.get("main", {})
        weather = weather_data.get("weather", [{}])[0]
        wind = weather_data.get("wind", {})

        temp = main.get("temp", 0)
        humidity = main.get("humidity", 0)
        wind_speed = wind.get("speed", 0)
        description = weather.get("main", "").lower()

        if (
            "tornado" in description or "hurricane" in description or
            ("thunderstorm" in description and wind_speed > 50) or
            temp < -40 or temp > 55 or wind_speed > 80
        ):
            return AlertLevel.DANGER

        if (
            "thunderstorm" in description or "heavy rain" in description or
            "heavy snow" in description or wind_speed > 40 or
            temp < -20 or temp > 45 or (humidity > 90 and temp > 30)
        ):
            return AlertLevel.WARNING

        return AlertLevel.SAFE

    def process_query(self, query: str) -> dict:
        """Process weather query"""
        import random
        
        query_lower = query.lower()
        location = self.last_location

        location_keywords = ["in ", "at ", "near ", "around ", "check ", "weather in"]
        for keyword in location_keywords:
            if keyword in query_lower:
                parts = query_lower.split(keyword)
                if len(parts) > 1:
                    potential_location = parts[1].strip().split(" ")[0]
                    if potential_location and potential_location not in ["here", "there"]:
                        location = potential_location.capitalize()
                        break

        weather_data = self.get_weather(location)
        
        if "error" in weather_data:
            return {
                "alert": "SAFE",
                "text": f"Error: {weather_data['error']}",
                "greeting": "Oops!",
                "error": True
            }

        alert_level = self.assess_danger_level(weather_data)
        main = weather_data.get("main", {})
        weather = weather_data.get("weather", [{}])[0]
        wind = weather_data.get("wind", {})

        city = weather_data.get("name", "Unknown")
        temp = main.get("temp", 0)
        feels_like = main.get("feels_like", 0)
        humidity = main.get("humidity", 0)
        wind_speed = wind.get("speed", 0)
        description = weather.get("description", "").title()

        alert_messages = {
            AlertLevel.SAFE: "All clear! Everything looks perfect! 🌞",
            AlertLevel.WARNING: "⚠️ WARNING! Severe weather nearby! Stay alert!",
            AlertLevel.DANGER: "🚨 RED ALERT! SEEK SHELTER IMMEDIATELY!",
        }

        text = f"""
📍 {city}
{description}

🌡️  Temperature: {temp}°C
Feel's like: {feels_like}°C
💧 Humidity: {humidity}%
💨 Wind: {wind_speed} m/s

{alert_messages[alert_level]}
"""

        return {
            "alert": alert_level.name,
            "text": text.strip(),
            "greeting": random.choice(self.personality),
            "source": weather_data.get("source", "unknown"),
            "error": False
        }


# Flask Web App
from flask import Flask, request, jsonify, render_template_string, send_from_directory

app = Flask(__name__)
sparky = None

# Service Worker
SERVICE_WORKER = """
const CACHE_NAME = 'sparky-v1';
const urlsToCache = [
  '/',
  '/manifest.json',
  '/offline'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request).catch(() => {
        return caches.match('/offline');
      });
    })
  );
});
"""

# Manifest for PWA
MANIFEST = {
    "name": "Sparky the Weatherbug",
    "short_name": "Sparky",
    "description": "AI Weather Assistant with Voice Activation",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#667eea",
    "scope": "/",
    "icons": [
        {
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 192 192'><text y='150' font-size='150'>🐞</text></svg>",
            "sizes": "192x192",
            "type": "image/svg+xml",
            "purpose": "any"
        }
    ],
    "categories": ["weather"],
    "screenshots": [
        {
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 540 720'><rect fill='%23667eea' width='540' height='720'/><text x='270' y='360' font-size='100' text-anchor='middle' fill='white'>🐞</text></svg>",
            "sizes": "540x720",
            "form_factor": "narrow"
        }
    ]
}

# Main HTML
MAIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#667eea">
    <meta name="description" content="Sparky the Weatherbug - AI Weather Assistant with Voice Activation">
    <link rel="manifest" href="/manifest.json">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='75' font-size='75'>🐞</text></svg>">
    <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 180 180'><text y='135' font-size='135'>🐞</text></svg>">
    <title>Sparky the Weatherbug</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .app-container {
            width: 100%;
            max-width: 600px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        @media (max-width: 768px) {
            .app-container {
                max-width: 100%;
                border-radius: 10px;
                min-height: auto;
            }
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 5px;
        }
        
        header p {
            opacity: 0.9;
            font-size: 0.95em;
        }
        
        main {
            flex: 1;
            padding: 30px 20px;
            overflow-y: auto;
        }
        
        .input-section {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 2px solid #667eea;
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #764ba2;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        button {
            padding: 15px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
            font-size: 1em;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .mic-button {
            width: 50px;
            height: 50px;
            padding: 0;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
        }
        
        .mic-button.listening {
            animation: micPulse 0.5s infinite;
            background: linear-gradient(135deg, #ff6b6b 0%, #ff0000 100%);
        }
        
        @keyframes micPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .response-section {
            display: none;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .alert-display {
            font-size: 4em;
            text-align: center;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .bug-display {
            font-size: 3em;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .weather-text {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            line-height: 1.8;
            margin-bottom: 15px;
            white-space: pre-wrap;
            font-size: 0.95em;
        }
        
        .info-bar {
            background: #f0f4ff;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.85em;
            color: #667eea;
            text-align: center;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            display: none;
        }
        
        .loading {
            text-align: center;
            display: none;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading p {
            color: #667eea;
            margin-top: 10px;
        }
        
        footer {
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            font-size: 0.85em;
            color: #666;
            border-top: 1px solid #eee;
        }
        
        .install-button {
            width: 100%;
            margin-top: 20px;
            display: none;
        }
        
        @supports (display: standalone) {
            @media (display-mode: standalone) {
                .install-button {
                    display: none !important;
                }
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <header>
            <h1>🐞 Sparky</h1>
            <p>Weather Assistant</p>
        </header>
        
        <main>
            <div class="input-section">
                <input 
                    type="text" 
                    id="query" 
                    placeholder="Ask about the weather..." 
                    autocomplete="off"
                >
                <button id="micButton" class="mic-button" title="Voice input">🎤</button>
            </div>
            
            <div id="error" class="error"></div>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Sparky is checking the weather...</p>
            </div>
            
            <div id="response" class="response-section">
                <div id="alert" class="alert-display"></div>
                <div class="bug-display">🐞</div>
                <div id="text" class="weather-text"></div>
                <div id="info" class="info-bar"></div>
            </div>
            
            <button id="installButton" class="install-button">📲 Install App</button>
        </main>
        
        <footer>
            <p>Stay safe and always check the weather! 🐛✨</p>
            <p id="version">Powered by WeatherBug & OpenWeatherMap</p>
        </footer>
    </div>
    
    <script>
        // Service Worker Registration
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW registration failed'));
        }
        
        // Speech Recognition
        const recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognizer = null;
        let isListening = false;
        
        if (recognition) {
            recognizer = new recognition();
            recognizer.continuous = false;
            recognizer.interimResults = false;
            recognizer.language = 'en-US';
            
            recognizer.onstart = () => {
                isListening = true;
                document.getElementById('micButton').classList.add('listening');
            };
            
            recognizer.onend = () => {
                isListening = false;
                document.getElementById('micButton').classList.remove('listening');
            };
            
            recognizer.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                document.getElementById('query').value = transcript;
                queryWeather(transcript);
            };
            
            recognizer.onerror = (event) => {
                console.error('Speech error:', event.error);
            };
        }
        
        document.getElementById('micButton').addEventListener('click', () => {
            if (recognizer) {
                if (isListening) {
                    recognizer.stop();
                } else {
                    document.getElementById('query').value = '';
                    recognizer.start();
                }
            }
        });
        
        document.getElementById('query').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                queryWeather(e.target.value);
            }
        });
        
        async function queryWeather(query) {
            if (!query.trim()) return;
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('response').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            try {
                const res = await fetch('/api/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await res.json();
                document.getElementById('loading').style.display = 'none';
                
                if (data.error) {
                    document.getElementById('error').textContent = data.text;
                    document.getElementById('error').style.display = 'block';
                } else {
                    displayWeather(data);
                }
            } catch (e) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('error').textContent = 'Error: ' + e.message;
                document.getElementById('error').style.display = 'block';
            }
        }
        
        function displayWeather(data) {
            const alerts = { SAFE: '🟢', WARNING: '🟡', DANGER: '🔴' };
            document.getElementById('alert').textContent = alerts[data.alert];
            document.getElementById('text').textContent = data.text;
            document.getElementById('info').textContent = 'API: ' + data.source;
            document.getElementById('response').style.display = 'block';
        }
        
        // Load initial weather
        window.addEventListener('load', () => {
            fetch('/api/weather').then(r => r.json()).then(displayWeather).catch(console.error);
        });
        
        // Install PWA Button
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            document.getElementById('installButton').style.display = 'block';
        });
        
        document.getElementById('installButton').addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log('User response to the install prompt:', outcome);
                deferredPrompt = null;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(MAIN_HTML)

@app.route('/manifest.json')
def manifest():
    return jsonify(MANIFEST)

@app.route('/sw.js')
def service_worker():
    return SERVICE_WORKER, 200, {'Content-Type': 'application/javascript'}

@app.route('/api/query', methods=['POST'])
def api_query():
    query = request.json.get('query', '')
    if not query:
        return jsonify({'error': True, 'text': 'No query provided'})
    
    response = sparky.process_query(query)
    return jsonify(response)

@app.route('/api/weather', methods=['GET'])
def api_weather():
    response = sparky.process_query("What's the weather?")
    return jsonify(response)

@app.route('/offline')
def offline():
    return "Offline - Please check your connection", 200

def run_app(api_key: str = None, port: int = 5000, open_browser: bool = True):
    """Run the Sparky web app"""
    global sparky
    
    try:
        sparky = SparkyWeatherAssistant(api_key=api_key)
        
        print("\n" + "="*70)
        print("🐞 SPARKY THE WEATHERBUG - FULL WEB APP")
        print("="*70)
        print(f"\n✨ Features:")
        print(f"  🎤 Voice Activation - Say weather questions")
        print(f"  🟢🟡🔴 Dynamic Shell Color Alerts")
        print(f"  🌤️  Real-time Weather Data - {('WeatherBug' if sparky.use_weatherbug else 'OpenWeatherMap')}")
        print(f"  📱 Progressive Web App - Install on homescreen")
        print(f"  💬 Interactive AI Responses")
        print(f"  🌐 Works Offline - Cached data")
        print(f"\n🌐 Web App URL: http://localhost:{port}")
        print(f"📱 Mobile: http://YOUR_IP:{port}")
        print(f"📲 iPhone: Share → Add to Home Screen")
        print(f"💻 Desktop: Install as App")
        print(f"\n" + "="*70 + "\n")
        
        if open_browser:
            threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()
        
        app.run(debug=False, port=port, host='0.0.0.0')
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print(f"\nPlease set WEATHERBUG_API_KEY or OPENWEATHER_API_KEY in .env")
        exit(1)
    except KeyboardInterrupt:
        print("\n\n🐛 Sparky says: Stay safe! Goodbye! 🐛\n")
        exit(0)


if __name__ == '__main__':
    import sys
    
    api_key = sys.argv[1] if len(sys.argv) > 1 else None
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    
    run_app(api_key=api_key, port=port, open_browser=True)
