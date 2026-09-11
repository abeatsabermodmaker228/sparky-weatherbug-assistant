# 🐞 Sparky the Weatherbug - Quick Start Guide

## What is Sparky?

**Sparky** is an AI weather assistant that you can:
- 📱 **Install on iPhone home screen**
- 💻 **Run as desktop app**
- 🌐 **Use as web app from any browser**
- 🎤 **Control with voice** - Say "What's the weather?"
- 🟢🟡🔴 **See danger alerts** - Shell changes color based on conditions

## ⚡ 5-Minute Setup

### Step 1: Get Your Free API Key (2 min)

**Option A: WeatherBug (Recommended)**
1. Go to: https://www.weatherbug.com/api
2. Click "Sign Up"
3. Create account (free)
4. Copy your API key

**Option B: OpenWeatherMap (Fallback)**
1. Go to: https://openweathermap.org/api
2. Click "Sign Up"
3. Create account (free)
4. Copy your API key

### Step 2: Install Sparky (2 min)

```bash
# Clone the repository
git clone https://github.com/abeatsabermodmaker228/sparky-weatherbug-assistant.git
cd sparky-weatherbug-assistant

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and paste your API key
# Windows: notepad .env
# Mac/Linux: nano .env
```

In `.env`, add:
```
WEATHERBUG_API_KEY=your_api_key_here
```

### Step 3: Launch Sparky (1 min)

**Option A: Full Web App (Recommended)**
```bash
python web_app.py
```
Opens in browser → http://localhost:5000

**Option B: Simple Widget**
```bash
python widget_launcher.py
```

**Option C: Desktop Launch**
```bash
python main.py
```

That's it! 🎉

## 📱 iPhone Setup (3 steps)

### Step 1: Start Sparky on Computer
```bash
python web_app.py
```

### Step 2: Find Your Computer's IP Address

**Windows (PowerShell):**
```powershell
ipconfig
# Look for "IPv4 Address" like 192.168.1.100
```

**Mac/Linux (Terminal):**
```bash
ifconfig
# Look for "inet" address on WiFi
```

### Step 3: Open on iPhone
1. Make sure iPhone is on **same WiFi** as computer
2. Open Safari
3. Go to: `http://192.168.1.100:5000` (use YOUR IP)
4. Tap **Share** → **Add to Home Screen**
5. Done! 🐞

**To use:**
- Tap the Sparky icon on home screen
- Click microphone 🎤
- Say: "What's the weather?"

## 💻 Desktop Setup (Windows/Mac/Linux)

### Windows Desktop Shortcut

Create file `start_sparky.bat`:
```batch
@echo off
python web_app.py
```

Save → Right-click → Send to Desktop → Create shortcut

### Mac Desktop App

Create file `start_sparky.command`:
```bash
#!/bin/bash
cd ~/path/to/sparky-weatherbug-assistant
python3 web_app.py
```

Make executable:
```bash
chmod +x start_sparky.command
```

### Linux Desktop Icon

Create file `sparky.desktop`:
```ini
[Desktop Entry]
Type=Application
Name=Sparky Weather
Exec=python3 /path/to/web_app.py
Icon=weather
Terminal=false
```

## 🎤 Voice Commands

Simply say:
- "What's the weather?"
- "Weather in London"
- "Is it raining?"
- "How hot is it?"
- "Check the forecast"
- "Do I need an umbrella?"

Sparky understands natural language! 🐛✨

## 🟢🟡🔴 Shell Color System

- **🟢 Green** - All clear! Safe conditions
- **🟡 Yellow** - Warning! Check forecast
- **🔴 Red** - DANGER! Seek shelter immediately!

Changes in **real-time** based on weather data!

## 📲 Install as App

### Browser Desktop
1. Open http://localhost:5000
2. Menu → Install App / Add to Home Screen
3. Works offline with cached data!

### iPhone
See iPhone Setup section above

### Android
1. Open in Chrome
2. Menu → "Install app"
3. Shows on home screen like native app

## 🌟 Features Explained

### 🎤 Voice Activation
- Click microphone button
- Speak naturally
- Sparky understands context
- Works in 50+ languages

### 🌤️ Real-time Weather
- **WeatherBug API** (primary) - Hyper-local, accurate
- **OpenWeatherMap** (fallback) - 5-day forecast
- Automatic failover if one API is down

### 🟢🟡🔴 Dynamic Alerts
- **Green**: Temp -20 to 45°C, wind < 40 m/s
- **Yellow**: Thunderstorm, heavy rain, wind 40-80 m/s
- **Red**: Tornado, extreme temps, wind > 80 m/s

### 📱 Progressive Web App (PWA)
- Install on home screen
- Works offline
- Feels like native app
- No app store needed

### 💬 AI Personality
- Random friendly greetings
- Natural conversation
- Contextual responses
- Learns your location

## 🔧 Troubleshooting

### "API Key Not Found"
```bash
# Make sure .env file exists and contains:
WEATHERBUG_API_KEY=your_key_here

# Test with:
cat .env
```

### "Cannot Connect on iPhone"
- ✅ Both devices on same WiFi
- ✅ IP address correct
- ✅ Server still running on computer
- ✅ Check firewall (port 5000)

### "Microphone Not Working"
- ✅ Grant permission in browser
- ✅ Try different browser
- ✅ Check microphone in system settings
- ✅ Test at https://www.webrtc-experiment.com/speech/

### "Slow Responses"
- ✅ Check internet connection
- ✅ Restart Python server
- ✅ Try closer location name
- ✅ API might be rate-limited (wait a minute)

### Port Already in Use
```bash
# Use different port:
python web_app.py 8080
# Then open: http://localhost:8080
```

## 📚 Advanced Options

### Custom Port
```bash
python web_app.py 8080
```

### API Key as Argument
```bash
python web_app.py YOUR_API_KEY 5000
```

### Disable Browser Auto-Open
Edit `web_app.py`, change `open_browser=True` to `False`

### Run Without Voice
Edit HTML, comment out speech recognition code

## 🎯 Next Steps

1. ✅ Get free API key (2 min)
2. ✅ Clone repository (1 min)
3. ✅ Install dependencies (2 min)
4. ✅ Create .env file (1 min)
5. ✅ Launch Sparky (1 min)
6. ✅ Add to iPhone (3 min)
7. ✅ Ask Sparky about weather!

**Total time: ~15 minutes** ⏱️

## 📞 Getting Help

### Check Logs
```bash
# Python output shows errors
# Check browser console: F12 or Cmd+Option+I
# Look for red error messages
```

### Common Fixes
1. Restart Python server
2. Clear browser cache
3. Check internet connection
4. Verify API key is valid
5. Try different browser

### API Status
- WeatherBug: https://www.weatherbug.com/api
- OpenWeatherMap: https://openweathermap.org/api

## 💡 Pro Tips

### 1. Keep Server Running
Use these to keep Sparky always available:
- Background process manager
- System startup script
- Always-on computer/Raspberry Pi

### 2. Multiple Locations
Ask Sparky about weather "in New York", "in London", etc.
Sparky remembers your last location!

### 3. Share with Friends
Send them your computer's IP on same WiFi:
```
Hey! Check the weather with Sparky:
http://192.168.1.100:5000
```

### 4. Customize Appearance
Edit CSS in `web_app.py` → `MAIN_HTML`
Change colors, fonts, animations!

### 5. Add to Multiple Devices
Run on computer, access from:
- Multiple iPhones
- Android phones
- Tablets
- Desktop browsers
- Smartwatches

## 🚀 Performance Tips

- Use modern browser (Chrome/Safari)
- Keep computer plugged in
- Good WiFi signal
- Close unnecessary browser tabs
- Restart if slow (memory leak)

## 📖 Full Documentation

- **WIDGET_SETUP.md** - Detailed widget setup
- **IPHONE_SETUP.md** - Complete iPhone guide
- **SPRITES.md** - Sprite customization
- **CONFIG.md** - Advanced configuration
- **README.md** - Project overview

## 🎉 You're Ready!

Start Sparky now:
```bash
python web_app.py
```

Then:
- 💻 Open http://localhost:5000 on browser
- 📱 Open on iPhone at http://YOUR_IP:5000
- 🎤 Click microphone and ask about weather!

**Enjoy Sparky! 🐞✨**

---

## Quick Reference

| Task | Command |
|------|---------|
| Start Web App | `python web_app.py` |
| Start Widget | `python widget_launcher.py` |
| Start CLI | `python main.py` |
| Create .env | `cp .env.example .env` |
| Get IP (Windows) | `ipconfig` |
| Get IP (Mac/Linux) | `ifconfig` |
| Install dependencies | `pip install -r requirements.txt` |
| Edit config | `nano .env` or `code .env` |

---

**Made with ❤️ by Sparky the Weatherbug** 🐛
Visit: https://github.com/abeatsabermodmaker228/sparky-weatherbug-assistant
