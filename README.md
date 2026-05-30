# 🚪 Mom Detector (Battery-Powered Edition)

> Door opens → PC instantly switches to a random educational site. Built with ESP32 + Python + Deep Sleep.

---

## 🛒 Parts List

| Part                               | Where to Buy              | Cost   |
| ---------------------------------- | ------------------------- | ------ |
| ESP32 Dev Board (WROOM-32)         | Amazon / AliExpress       | ~$8    |
| Reed Switch (NO type)              | Amazon                    | ~$5    |
| Magnet                             | Included with reed switch | —      |
| AMS1117-3.3V Regulator             | Amazon                    | ~$0.50 |
| 2× 100µF electrolytic capacitors   | Amazon                    | ~$0.50 |
| 2× 2xAA battery packs (or 1× 4xAA) | You have these            | —      |
| Jumper wires                       | Amazon                    | ~$2    |

**Total: ~$16**

---

## ⚡ Wiring

See `WIRING_DIAGRAM.svg` or the diagram in the documentation.

**Quick summary:**

- Battery pack(s) in series → AMS1117 regulator → ESP32 VIN
- Reed switch between GPIO 14 and GND
- Deep sleep mode uses ~10 µA standby (6-12 months on batteries)

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

### Step 3 — Configure Credentials (IMPORTANT!)

⚠️ **Do NOT hardcode WiFi passwords in the sketch** — use a separate `credentials.h` file instead. This keeps your password out of GitHub.

**Setup:**

1. Download or clone this repo
2. In the same folder as `esp32-mom-detector-battery.ino`, create a new file called `credentials.h`
3. Copy this template into it:

```cpp
// credentials.h - EXCLUDED FROM GIT
// Fill in YOUR values below

#ifndef CREDENTIALS_H
#define CREDENTIALS_H

const char* SSID = "YOUR_WIFI_NAME";
const char* PASSWORD = "YOUR_WIFI_PASSWORD";
const char* PC_IP = "192.168.1.42";       // Replace with your PC's IPv4 from Step 2
const int PC_PORT = 5555;

#endif
```

**Fill in:**

- `YOUR_WIFI_NAME` — your Wi-Fi network name (e.g., `"HomeNetwork"`)
- `YOUR_WIFI_PASSWORD` — your Wi-Fi password
- `192.168.1.42` — the IPv4 address you found in Step 2
- `5555` — leave this alone unless you changed it in `mom_detector.py`

**Why this approach?**

- The `.gitignore` automatically excludes `credentials.h`, so your password never gets pushed to GitHub
- If you clone this repo again on another device, you just create a new `credentials.h` with that device's info
- The sketch includes `credentials.h` and uses the variables from it

---

### Step 4 — Flash the ESP32

The sketch is in `esp32-mom-detector-battery.ino`. After creating `credentials.h`:

**Upload:**

1. Plug ESP32 into PC via USB
2. `Tools > Board` → select **ESP32 Dev Module**
3. `Tools > Port` → select the COM port that appeared
4. Click **Upload** (→ arrow)
5. If stuck at `Connecting....` → hold the **BOOT** button on the ESP32 until it starts uploading

**Verify it works:**

- Open `Tools > Serial Monitor`, set baud to **115200**
- You should see `WiFi connected!` and `Going to deep sleep...`
- Open your door → ESP32 wakes, connects, sends alert to PC
- Random educational site opens on your PC

---

### Step 5 — Python Server (on your PC)

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

### Step 6 — Auto-Start on Boot (Windows)

Open **PowerShell as Administrator** (right-click Start → _Windows PowerShell (Admin)_).

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

- [ ] `credentials.h` created with YOUR WiFi + PC IP filled in
- [ ] ESP32 wired (Pin 14 + GND to reed switch)
- [ ] Reed switch on door frame (NO type), magnet on door
- [ ] Arduino IDE installed + ESP32 board package installed
- [ ] Code flashed — Serial Monitor shows `WiFi connected!`
- [ ] `mom_detector.py` saved somewhere permanent
- [ ] Flask installed (`pip install flask`)
- [ ] Python server auto-start task registered via PowerShell
- [ ] `netstat` confirms port 5555 is listening
- [ ] Open door → random site opens on PC ✅

---

## 🔋 Battery Life Expectations

With **deep sleep** enabled (this version):

- **Active time:** ~2 seconds per door open (WiFi + HTTP request)
- **Sleep time:** 99.8% of the time (~10 µA draw)
- **Expected life:** **6-12 months on 2×2xAA packs (6V)**

Without deep sleep (original version):

- Constant WiFi = 80+ mA draw
- Expected life: 1-2 weeks

---

## 🔧 Troubleshooting

| Problem                          | Fix                                                                                                             |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Upload stuck at `Connecting....` | Hold **BOOT** button on ESP32 while uploading                                                                   |
| No COM port in Arduino IDE       | Install **CP2102** or **CH340** USB drivers (Google your board's chip)                                          |
| ESP32 won't connect to Wi-Fi     | Make sure it's **2.4 GHz** — ESP32 doesn't support 5 GHz                                                        |
| Can't find `credentials.h` error | Make sure the file is in the same folder as `.ino` file, not in a subfolder                                     |
| PC not reachable from ESP32      | Run `ipconfig` again — your IP may have changed. Set a static IP in Windows network settings to fix permanently |
| Port 5555 not showing in netstat | Make sure `mom_detector.py` is actually running. Check Task Scheduler.                                          |
| Flask not found                  | Run `pip install flask` again, or try `pip3 install flask`                                                      |
| False triggers waking ESP32      | Reed switch might be too close to magnet — increase distance slightly                                           |

---

## 📝 Notes

- **NO vs NC:** This uses a **Normally Open (NO)** reed switch. Door closed = magnet holds it closed. Door open = magnet pulls away, switch opens, triggers GPIO interrupt.
- **2×2xAA in series:** Connect pack 1's + to pack 2's −. You now have 6V between pack 1's − and pack 2's +.
- **Customizing sites:** Edit the `SITES` list in `mom_detector.py` to add/remove random sites.
- **Changing port:** If you use a different port, update `PC_PORT` in `credentials.h` AND the `app.run(port=5555)` line in `mom_detector.py`.
