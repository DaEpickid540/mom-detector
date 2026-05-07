# 🚪 Mom Detector
> Door opens → PC instantly switches to a random educational site. Built with ESP32 + Python.

---

## 🛒 Parts List

| Part | Where to Buy | Cost |
|------|-------------|------|
| ESP32 Dev Board (WROOM-32) | Amazon / AliExpress | ~$8 |
| Reed Switch + Magnet (NO type) | Amazon (pack of 10) | ~$3 |
| Jumper wires (Male-Male) | Amazon | ~$3 |
| Micro USB cable | You have one | — |

**Total: ~$14**

---

## ⚡ Wiring

Reed switches have no polarity — just connect both wires anywhere.

```
ESP32 Pin 14  ──── [Reed Switch] ──── ESP32 GND
```

**Mounting:**
- Stick the **magnet** on the moving door
- Stick the **reed switch** on the door **frame**, aligned with the magnet
- Use double-sided tape or hot glue

```
CLOSED (safe):          OPEN (trigger!):
Frame    Door           Frame         Door
[Switch][Mag]    →      [Switch]  |  [Mag]
```

---

## 💻 Software Setup

### Step 1 — Arduino IDE

1. Download **Arduino IDE 2** → [arduino.cc/en/software](https://arduino.cc/en/software)
2. Open it → `File > Preferences`
3. Paste this into **Additional Boards Manager URLs**:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Go to `Tools > Board > Boards Manager` → search **esp32** → install **esp32 by Espressif Systems**

---

### Step 2 — Find Your PC's Local IP

Open **Command Prompt** and run:
```
ipconfig
```
Look for **IPv4 Address** under your Wi-Fi adapter. It'll look like `192.168.1.42`. Save this for the next step.

> ⚠️ Your ESP32 and PC must be on the **same Wi-Fi network**.

---

### Step 3 — Flash the ESP32

Create a new sketch in Arduino IDE and paste this code:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid     = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* pcIP     = "YOUR_PC_IP_HERE";   // e.g. "192.168.1.42"
const int   pcPort   = 5555;

const int DOOR_PIN = 14;
bool lastState = HIGH;
unsigned long lastTrigger = 0;

void setup() {
  Serial.begin(115200);
  pinMode(DOOR_PIN, INPUT_PULLUP);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
}

void loop() {
  bool currentState = digitalRead(DOOR_PIN);

  // Door opened = magnet pulled away = pin goes HIGH
  if (currentState == HIGH && lastState == LOW && millis() - lastTrigger > 3000) {
    lastTrigger = millis();
    Serial.println("Door opened! Alerting PC...");

    HTTPClient http;
    String url = "http://" + String(pcIP) + ":" + String(pcPort) + "/trigger";
    http.begin(url);
    int code = http.GET();
    Serial.println("Response code: " + String(code));
    http.end();
  }

  lastState = currentState;
  delay(50);
}
```

**Fill in:**
- `YOUR_WIFI_NAME` — your Wi-Fi SSID
- `YOUR_WIFI_PASSWORD` — your Wi-Fi password
- `YOUR_PC_IP_HERE` — the IP you found in Step 2

**Upload:**
1. Plug ESP32 into PC via USB
2. `Tools > Board` → select **ESP32 Dev Module**
3. `Tools > Port` → select the COM port that appeared
4. Click **Upload** (→ arrow)
5. If stuck at `Connecting....` → hold the **BOOT** button on the ESP32 until it starts uploading

**Verify it works:**
- Open `Tools > Serial Monitor`, set baud to **115200**
- You should see `WiFi connected!`

> **Reed switch reversed?** If the trigger fires when the door is *closed*, swap `HIGH` and `LOW` in the `if` condition.

---

### Step 4 — Python Server

**Install Flask (one time):**
```
pip install flask
```

**Create the file.** Save this as `mom_detector.py` somewhere permanent, like:
```
C:\Users\YourName\Documents\mom_detector\mom_detector.py
```

```python
from flask import Flask
import webbrowser, threading, random

app = Flask(__name__)

SITES = [
    # School platforms
    "https://app.schoology.com",
    "https://classroom.google.com",
    "https://docs.google.com",
    "https://drive.google.com",
    # Coding / your projects
    "https://github.com/DaEpickid540",
    "https://codehs.com",
    "https://code.org",
    "https://replit.com",
    "https://leetcode.com",
    # Educational
    "https://www.khanacademy.org",
    "https://brilliant.org",
    "https://www.codecademy.com",
    "https://www.coursera.org",
    "https://www.edx.org",
    # Reference / tools
    "https://www.desmos.com/calculator",
    "https://www.wolframalpha.com",
    "https://quizlet.com",
    "https://www.duolingo.com",
    # School-y looking sites
    "https://www.commonlit.org",
    "https://www.ixl.com",
    "https://www.typing.com",
    "https://scratch.mit.edu",
]

@app.route('/trigger')
def trigger():
    url = random.choice(SITES)
    print(f"[MOM DETECTED] Opening → {url}")
    threading.Thread(target=lambda: webbrowser.open_new_tab(url)).start()
    return "ok", 200

if __name__ == '__main__':
    print("Mom Detector running on port 5555...")
    app.run(host='0.0.0.0', port=5555)
```

**Test it manually:**
```
python "C:\Users\YourName\Documents\mom_detector\mom_detector.py"
```
Then open `http://localhost:5555/trigger` in your browser — a random site should open.

---

### Step 5 — Auto-Start on Boot

Open **PowerShell as Administrator** (right-click Start → *Windows PowerShell (Admin)*).

Run this block, replacing the path with where you actually saved the file:

```powershell
$pyPath = "C:\Users\YourName\Documents\mom_detector\mom_detector.py"

# Create a hidden launcher (pythonw = no visible terminal window)
$batPath = "$env:APPDATA\mom_detector_launch.bat"
Set-Content $batPath "@echo off`npythonw `"$pyPath`""

# Register with Task Scheduler to run at login
$action   = New-ScheduledTaskAction -Execute $batPath
$trigger  = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden
Register-ScheduledTask -TaskName "MomDetector" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force

Write-Host "Done! Will auto-start on next login."
```

**Start it right now without rebooting:**
```powershell
Start-ScheduledTask -TaskName "MomDetector"
```

**Confirm it's running:**
```
netstat -an | findstr 5555
```
You should see a line with `0.0.0.0:5555` — that means it's live.

**Remove it later:**
```powershell
Unregister-ScheduledTask -TaskName "MomDetector" -Confirm:$false
```

---

## ✅ Final Checklist

- [ ] ESP32 wired (Pin 14 + GND to reed switch)
- [ ] Reed switch on door frame, magnet on door
- [ ] Arduino IDE installed + ESP32 board package installed
- [ ] Code flashed with your Wi-Fi + PC IP filled in
- [ ] Serial Monitor shows `WiFi connected!`
- [ ] `mom_detector.py` saved somewhere permanent
- [ ] Flask installed (`pip install flask`)
- [ ] Auto-start task registered via PowerShell
- [ ] `netstat` confirms port 5555 is listening
- [ ] Open door → random site opens on PC ✅

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| Upload stuck at `Connecting....` | Hold **BOOT** button on ESP32 while uploading |
| No COM port in Arduino IDE | Install **CP2102** or **CH340** USB drivers (Google your board's chip) |
| ESP32 won't connect to Wi-Fi | Make sure it's **2.4 GHz** — ESP32 doesn't support 5 GHz |
| Door triggers when closed, not open | Swap `HIGH`/`LOW` in the `if` condition in the sketch |
| PC not reachable from ESP32 | Re-run `ipconfig` — your IP may have changed. Set a static IP in Windows network settings to fix permanently |
| Port 5555 not showing in netstat | `pythonw` might not be in PATH — try full path: `C:\Python3x\pythonw.exe` |
| Flask not found | Run `pip install flask` again, or try `pip3 install flask` |
