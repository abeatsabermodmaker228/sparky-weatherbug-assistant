#!/usr/bin/env python3
"""
Sparky the Weatherbug - Standalone Web App
No API keys, no setup, completely self-contained
Works with built-in mock weather data and local API
"""

import os
from datetime import datetime, timedelta
from enum import Enum
from flask import Flask, request, jsonify, render_template_string
import random
import webbrowser
import threading

app = Flask(__name__)

class AlertLevel(Enum):
    """Alert levels for weather conditions"""
    SAFE = "🟢"
    WARNING = "🟡"
    DANGER = "🔴"


# Mock Weather Data - Realistic examples for different locations
WEATHER_DATABASE = {
    "london": {
        "name": "London",
        "country": "UK",
        "temp": 18,
        "feels_like": 16,
        "humidity": 65,
        "wind_speed": 12,
        "wind_deg": 270,
        "pressure": 1013,
        "description": "Partly Cloudy",
        "alert": AlertLevel.SAFE
    },
    "new york": {
        "name": "New York",
        "country": "USA",
        "temp": 22,
        "feels_like": 20,
        "humidity": 55,
        "wind_speed": 15,
        "wind_deg": 180,
        "pressure": 1015,
        "description": "Clear Sky",
        "alert": AlertLevel.SAFE
    },
    "tokyo": {
        "name": "Tokyo",
        "country": "Japan",
        "temp": 25,
        "feels_like": 23,
        "humidity": 70,
        "wind_speed": 8,
        "wind_deg": 90,
        "pressure": 1012,
        "description": "Sunny",
        "alert": AlertLevel.SAFE
    },
    "paris": {
        "name": "Paris",
        "country": "France",
        "temp": 16,
        "feels_like": 15,
        "humidity": 75,
        "wind_speed": 20,
        "wind_deg": 270,
        "pressure": 1010,
        "description": "Rainy",
        "alert": AlertLevel.WARNING
    },
    "sydney": {
        "name": "Sydney",
        "country": "Australia",
        "temp": 28,
        "feels_like": 26,
        "humidity": 60,
        "wind_speed": 18,
        "wind_deg": 180,
        "pressure": 1018,
        "description": "Partly Cloudy",
        "alert": AlertLevel.SAFE
    },
    "toronto": {
        "name": "Toronto",
        "country": "Canada",
        "temp": 12,
        "feels_like": 10,
        "humidity": 80,
        "wind_speed": 25,
        "wind_deg": 360,
        "pressure": 1008,
        "description": "Cloudy",
        "alert": AlertLevel.WARNING
    },
    "dubai": {
        "name": "Dubai",
        "country": "UAE",
        "temp": 42,
        "feels_like": 45,
        "humidity": 35,
        "wind_speed": 5,
        "wind_deg": 90,
        "pressure": 1005,
        "description": "Hot & Sunny",
        "alert": AlertLevel.DANGER
    },
    "moscow": {
        "name": "Moscow",
        "country": "Russia",
        "temp": -5,
        "feels_like": -10,
        "humidity": 90,
        "wind_speed": 35,
        "wind_deg": 180,
        "pressure": 1000,
        "description": "Snowy",
        "alert": AlertLevel.WARNING
    },
    "bangkok": {
        "name": "Bangkok",
        "country": "Thailand",
        "temp": 32,
        "feels_like": 38,
        "humidity": 85,
        "wind_speed": 12,
        "wind_deg": 180,
        "pressure": 1012,
        "description": "Thunderstorm",
        "alert": AlertLevel.DANGER
    },
    "seattle": {
        "name": "Seattle",
        "country": "USA",
        "temp": 14,
        "feels_like": 12,
        "humidity": 88,
        "wind_speed": 22,
        "wind_deg": 270,
        "pressure": 1008,
        "description": "Heavy Rain",
        "alert": AlertLevel.WARNING
    }
}

GREETINGS = [
    "Stay safe out there, buddy! 🐛",
    "Sparky here with your weather update! ☀️",
    "Let's check what Mother Nature is cooking up! 🌦️",
    "Your friendly weatherbug reporting for duty! 🐞",
    "Time to buzz around and check the skies! 🐝",
    "Weather watch activated! 📡",
]


class SparkyWeatherAssistant:
    """Standalone Sparky Weather Assistant"""
    
    def __init__(self):
        self.last_location = "London"
    
    def find_location(self, query: str) -> str:
        """Find location from query"""
        query_lower = query.lower()
        
        # Direct matches
        for location in WEATHER_DATABASE.keys():
            if location in query_lower:
                return location
        
        # Fuzzy matching
        for location in WEATHER_DATABASE.keys():
            words = location.split()
            for word in words:
                if word in query_lower:
                    return location
        
        return self.last_location
    
    def get_weather(self, location: str) -> dict:
        """Get weather data"""
        location_key = location.lower()
        
        if location_key in WEATHER_DATABASE:
            self.last_location = location_key
            return WEATHER_DATABASE[location_key]
        
        # Fuzzy search
        for key in WEATHER_DATABASE.keys():
            if location_key.startswith(key[0:3]):
                self.last_location = key
                return WEATHER_DATABASE[key]
        
        # Default to last known location
        return WEATHER_DATABASE[self.last_location]
    
    def process_query(self, query: str) -> dict:
        """Process weather query"""
        if not query.strip():
            location = self.last_location
        else:
            location = self.find_location(query)
        
        weather = self.get_weather(location)
        
        # Add some randomness to simulate real data
        weather_copy = weather.copy()
        weather_copy['temp'] += random.randint(-2, 2)
        weather_copy['feels_like'] += random.randint(-2, 2)
        weather_copy['humidity'] += random.randint(-5, 5)
        weather_copy['wind_speed'] += random.randint(-3, 3)
        
        alert_messages = {
            AlertLevel.SAFE: "All clear! Everything looks perfect! 🌞",
            AlertLevel.WARNING: "⚠️ WARNING! Severe weather nearby! Stay alert!",
            AlertLevel.DANGER: "🚨 RED ALERT! Dangerous conditions ahead!",
        }
        
        text = f"""
📍 {weather_copy['name']}, {weather_copy['country']}
{weather_copy['description']}

🌡️  Temperature: {weather_copy['temp']}°C
Feels like: {weather_copy['feels_like']}°C
💧 Humidity: {weather_copy['humidity']}%
💨 Wind: {weather_copy['wind_speed']} m/s

{alert_messages[weather_copy['alert']]}
"""
        
        return {
            "alert": weather_copy['alert'].name,
            "text": text.strip(),
            "greeting": random.choice(GREETINGS),
            "source": "builtin",
            "error": False
        }


# Initialize Sparky
sparky = SparkyWeatherAssistant()

# HTML UI
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#667eea">
    <meta name="description" content="Sparky the Weatherbug - AI Weather Assistant">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>Sparky - Weather Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
            min-height: auto;
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
            padding: 30px 20px;
            flex: 1;
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
            font-family: monospace;
        }
        
        .locations-btn {
            width: 100%;
            margin-bottom: 20px;
            padding: 10px;
            font-size: 0.9em;
        }
        
        .location-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .location-btn {
            padding: 10px;
            font-size: 0.85em;
            background: #f0f4ff;
            color: #667eea;
            border: 1px solid #667eea;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .location-btn:hover {
            background: #667eea;
            color: white;
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
            
            <button id="locBtn" class="locations-btn">📍 Quick Locations</button>
            
            <div id="locationGrid" class="location-grid" style="display: none;">
                <button class="location-btn" onclick="queryWeather('London')">🇬🇧 London</button>
                <button class="location-btn" onclick="queryWeather('New York')">🇺🇸 New York</button>
                <button class="location-btn" onclick="queryWeather('Tokyo')">🇯🇵 Tokyo</button>
                <button class="location-btn" onclick="queryWeather('Paris')">🇫🇷 Paris</button>
                <button class="location-btn" onclick="queryWeather('Sydney')">🇦🇺 Sydney</button>
                <button class="location-btn" onclick="queryWeather('Dubai')">🇦🇪 Dubai</button>
                <button class="location-btn" onclick="queryWeather('Toronto')">🇨🇦 Toronto</button>
                <button class="location-btn" onclick="queryWeather('Moscow')">🇷🇺 Moscow</button>
            </div>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Sparky is checking the weather...</p>
            </div>
            
            <div id="response" class="response-section">
                <div id="alert" class="alert-display"></div>
                <div class="bug-display">🐞</div>
                <div id="text" class="weather-text"></div>
            </div>
        </main>
        
        <footer>
            <p>Stay safe and always check the weather! 🐛✨</p>
            <p>No API keys required • Works completely offline</p>
        </footer>
    </div>
    
    <script>
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
        
        document.getElementById('locBtn').addEventListener('click', function() {
            const grid = document.getElementById('locationGrid');
            grid.style.display = grid.style.display === 'none' ? 'grid' : 'none';
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
            document.getElementById('locationGrid').style.display = 'none';
            
            try {
                const res = await fetch('/api/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await res.json();
                document.getElementById('loading').style.display = 'none';
                displayWeather(data);
            } catch (e) {
                document.getElementById('loading').style.display = 'none';
                console.error('Error:', e);
            }
        }
        
        function displayWeather(data) {
            const alerts = { SAFE: '🟢', WARNING: '🟡', DANGER: '🔴' };
            document.getElementById('alert').textContent = alerts[data.alert];
            document.getElementById('text').textContent = data.text;
            document.getElementById('response').style.display = 'block';
        }
        
        // Load initial weather
        window.addEventListener('load', () => {
            fetch('/api/weather').then(r => r.json()).then(displayWeather).catch(console.error);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/query', methods=['POST'])
def api_query():
    query = request.json.get('query', '')
    response = sparky.process_query(query)
    return jsonify(response)

@app.route('/api/weather', methods=['GET'])
def api_weather():
    response = sparky.process_query("What's the weather?")
    return jsonify(response)

def run_app(port: int = 5000, open_browser: bool = True):
    """Run Sparky standalone"""
    print("\n" + "="*70)
    print("🐞 SPARKY THE WEATHERBUG - STANDALONE WEB APP")
    print("="*70)
    print("\n✨ Features:")
    print("  🎤 Voice Activation")
    print("  🟢🟡🔴 Dynamic Shell Color Alerts")
    print("  🌤️  Built-in Weather Data - No API keys needed!")
    print("  📱 Works on any device")
    print("  💬 Interactive AI Responses")
    print("\n🌐 Web App URL: http://localhost:" + str(port))
    print("📱 On another device: http://YOUR_IP:" + str(port))
    print("📲 iPhone: Share → Add to Home Screen")
    print("\n" + "="*70 + "\n")
    
    if open_browser:
        threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    app.run(debug=False, port=port, host='0.0.0.0')


if __name__ == '__main__':
    import sys
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    try:
        run_app(port=port, open_browser=True)
    except KeyboardInterrupt:
        print("\n\n🐛 Sparky says: Stay safe! Goodbye! 🐛\n")
        exit(0)
