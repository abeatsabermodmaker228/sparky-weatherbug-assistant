# iPhone & Mobile Setup Guide - Sparky Widget on Home Screen

## 🍎 Add Sparky to iPhone Home Screen

### Step 1: Start the Widget Server

On your computer:

```bash
python widget_launcher.py
```

The server will show:
```
🌐 Starting Widget Server on port 5000
📱 Open browser to: http://localhost:5000
```

### Step 2: Find Your Computer's IP Address

**On Windows (PowerShell):**
```powershell
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

**On Mac/Linux (Terminal):**
```bash
ifconfig
```
Look for "inet" address on your WiFi connection (e.g., 192.168.1.100)

### Step 3: Open on iPhone

1. Make sure iPhone is on **same WiFi network** as your computer
2. Open Safari on your iPhone
3. Go to: `http://YOUR_COMPUTER_IP:5000`
   - Example: `http://192.168.1.100:5000`
4. You should see Sparky widget!

### Step 4: Add to Home Screen

**Method A: Web Clip (Recommended)**

1. In Safari, tap the **Share** button (box with arrow)
2. Scroll down and tap **"Add to Home Screen"**
3. Name it "Sparky" (or whatever you like)
4. Tap **"Add"** in the top right
5. Sparky now appears on your home screen! 🐞

**Method B: Home Screen Shortcut**

1. Open **Shortcuts** app
2. Tap **"Create Shortcut"**
3. Add action: **"Open URL"**
4. Enter: `http://YOUR_COMPUTER_IP:5000`
5. Name it "Sparky"
6. Done!

### Step 5: Use Sparky on iPhone

1. Tap the Sparky icon on your home screen
2. Click the **microphone button** 🎤
3. **Say your question:**
   - "What's the weather?"
   - "Is it raining?"
   - "How hot is it in New York?"
4. **Grant microphone permission** if asked
5. Sparky responds! 🐞✨

## 🔧 Keep Widget Running

For Sparky to work on your iPhone, the **server must stay running** on your computer.

### Background Running (Windows)

**Option 1: Minimized Window**
- Let the Python window stay open (minimize it)
- Keep your computer awake/plugged in

**Option 2: Run as Service**
```batch
# Create sparky_service.bat
@echo off
:loop
python widget_launcher.py
goto loop
```

**Option 3: Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task → "Sparky Widget"
3. Trigger: "At system startup"
4. Action: Run `python widget_launcher.py`
5. Check "Run with highest privileges"

### Background Running (Mac)

Create `com.sparky.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sparky.widget</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/widget_launcher.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Install:
```bash
cp com.sparky.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.sparky.plist
```

### Background Running (Linux)

Create `sparky.service`:
```ini
[Unit]
Description=Sparky Weather Widget
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/sparky
ExecStart=/usr/bin/python3 widget_launcher.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Install:
```bash
sudo cp sparky.service /etc/systemd/system/
sudo systemctl enable sparky.service
sudo systemctl start sparky.service
```

## 📱 iOS Web App (PWA)

For a more app-like experience:

1. Open Sparky in Safari on iPhone
2. Tap **Share** → **"Add to Home Screen"**
3. It works **offline** after first load (cached)
4. Full screen experience
5. Feels like a native app!

## 🎤 Voice Commands on iPhone

The widget supports **voice recognition** on iPhone:

1. Tap the **microphone button** 🎤
2. Your iPhone's microphone activates
3. Speak naturally:
   - "What's the weather?"
   - "Weather in London"
   - "Is it cold outside?"
4. iPhone recognizes your speech
5. Sparky responds!

**Note:** Requires microphone permission - grant when asked

## 🔐 Secure Local Network

For best security:

### Option 1: Local Network Only (Safest)
- Keep server on private WiFi only
- Use strong WiFi password
- Disable when not in use

### Option 2: HTTPS/SSL (More Secure)

Install SSL certificate:
```bash
pip install pyopenssl
```

Generate certificate:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Update `widget.py`:
```python
app.run(ssl_context=('cert.pem', 'key.pem'))
```

Then access via: `https://YOUR_IP:5000`

### Option 3: Public Cloud (Advanced)

For remote access, use a service like:
- **ngrok** - Instant public URL
- **Cloudflare Tunnel** - Secure tunneling
- **SSH Port Forwarding** - Direct tunnel

## 📊 Firewall Settings

If Sparky won't connect from iPhone:

**Windows Firewall:**
1. Settings → Firewall → Allow apps through
2. Find Python or widget_launcher.py
3. Check "Private" networks
4. Allow

**Mac Firewall:**
1. System Preferences → Security & Privacy → Firewall
2. Click "Firewall Options"
3. Add Python to allowed apps

**Linux (UFW):**
```bash
sudo ufw allow 5000/tcp
```

## 🌐 Remote Access (Optional)

### Using ngrok (Free)

1. Download ngrok from ngrok.com
2. Run Sparky widget (port 5000)
3. In terminal:
```bash
./ngrok http 5000
```
4. Copy the public URL (e.g., https://abc123.ngrok.io)
5. Open on iPhone from anywhere!

### Using Cloudflare Tunnel (Free)

1. Install cloudflared
2. Run:
```bash
cloudflared tunnel --url http://localhost:5000
```
3. Get public URL
4. Access from iPhone anywhere

## ⚠️ Troubleshooting iPhone Connection

### "Cannot reach server"
- ✅ Computer and iPhone on **same WiFi**
- ✅ Check IP address is correct
- ✅ Python server is running
- ✅ Port 5000 is not blocked

### "Microphone not working"
- ✅ Grant microphone permission in Safari settings
- ✅ Check iPhone microphone works (Voice Memos app)
- ✅ Try another browser (Chrome, Firefox)

### "Slow responses"
- ✅ WiFi signal is strong
- ✅ Computer has good internet
- ✅ WeatherBug/OpenWeatherMap API is responsive

### "Widget keeps refreshing"
- ✅ WiFi connection dropped - reconnect
- ✅ Server crashed - restart `widget_launcher.py`
- ✅ Browser cache issue - refresh page

## 💡 Pro Tips

### 1. Siri Shortcut for Sparky
Create a custom Siri command:
1. Open Shortcuts app
2. Create new shortcut
3. Add "Open URL" with Sparky widget URL
4. Rename to "Ask Sparky"
5. Now say: "Hey Siri, Ask Sparky"

### 2. Add Multiple Instances
Need Sparky on different ports?
```bash
# Terminal 1
python widget_launcher.py 5000

# Terminal 2
python widget_launcher.py 5001
```

### 3. Custom Home Screen
- Use different colors for different locations
- Edit CSS in widget.py
- Change alert colors to match your iPhone theme

### 4. Always-On Computer
- Use Mac Mac Mini or Raspberry Pi
- Set to never sleep
- Runs 24/7 for always-on Sparky

## 📲 Widgets for Other Devices

### Android
Same process:
1. Start server on computer
2. Open in Chrome on Android
3. Menu → "Install app" or "Add to home screen"
4. Works as home screen widget!

### iPad
Same as iPhone - works great on larger screen

### macOS
Open in Safari → Share → Add to Dock

### Windows
Create Windows shortcut to `http://localhost:5000`

## 🎯 Next Steps

1. ✅ Start widget server on computer
2. ✅ Find computer IP address
3. ✅ Open in iPhone Safari
4. ✅ Add to home screen
5. ✅ Tap microphone and ask weather questions
6. ✅ Enjoy Sparky! 🐞✨

## Support

Having issues? Check:
1. WiFi connection (same network)
2. IP address correct
3. Server still running (`python widget_launcher.py`)
4. No firewall blocking port 5000
5. Browser permissions (microphone, location)

Enjoy your Sparky weather widget on iPhone! 🐞📱
