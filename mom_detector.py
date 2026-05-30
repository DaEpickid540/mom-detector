from flask import Flask, jsonify, request
import webbrowser
import threading
import json
import os
import random

app = Flask(__name__)

# Fix: use absolute path so sites.json always saves next to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SITES_FILE = os.path.join(SCRIPT_DIR, "sites.json")
DETECTOR_ENABLED = True

def load_sites():
    if os.path.exists(SITES_FILE):
        with open(SITES_FILE, 'r') as f:
            return json.load(f)
    defaults = [
        "https://app.schoology.com",
        "https://classroom.google.com",
        "https://docs.google.com",
        "https://drive.google.com",
        "https://github.com/DaEpickid540",
        "https://codehs.com",
        "https://code.org",
        "https://replit.com",
        "https://leetcode.com",
        "https://www.khanacademy.org",
        "https://brilliant.org",
        "https://www.codecademy.com",
        "https://www.coursera.org",
        "https://www.edx.org",
        "https://www.desmos.com/calculator",
        "https://www.wolframalpha.com",
        "https://quizlet.com",
        "https://www.duolingo.com",
        "https://www.commonlit.org",
        "https://www.ixl.com",
        "https://www.typing.com",
        "https://scratch.mit.edu",
    ]
    save_sites(defaults)
    return defaults

def save_sites(sites):
    with open(SITES_FILE, 'w') as f:
        json.dump(sites, f, indent=2)

SITES = load_sites()

# ── ROUTES ────────────────────────────────────────────

@app.route('/trigger')
def trigger():
    global DETECTOR_ENABLED, SITES
    if not DETECTOR_ENABLED:
        print("[BLOCKED] Mom Detector is disabled")
        return "disabled", 200
    if not SITES:
        print("[ERROR] No sites in list")
        return "error", 400
    url = random.choice(SITES)
    print(f"[DOOR OPENED] Opening -> {url}")
    threading.Thread(target=lambda: webbrowser.open_new_tab(url)).start()
    return "ok", 200

@app.route('/api/status')
def get_status():
    return jsonify({'enabled': DETECTOR_ENABLED, 'sites': SITES})

@app.route('/api/toggle', methods=['POST'])
def toggle_detector():
    global DETECTOR_ENABLED
    DETECTOR_ENABLED = not DETECTOR_ENABLED
    print(f"[STATUS] Mom Detector {'ENABLED' if DETECTOR_ENABLED else 'DISABLED'}")
    return jsonify({'enabled': DETECTOR_ENABLED})

@app.route('/api/add-site', methods=['POST'])
def add_site():
    global SITES
    data = request.json
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'URL cannot be empty'}), 400
    if url in SITES:
        return jsonify({'error': 'Site already exists'}), 400
    SITES.append(url)
    save_sites(SITES)
    print(f"[ADDED] {url}")
    return jsonify({'sites': SITES})

@app.route('/api/remove-site', methods=['POST'])
def remove_site():
    global SITES
    data = request.json
    url = data.get('url', '').strip()
    if url not in SITES:
        return jsonify({'error': 'Site not found'}), 400
    SITES.remove(url)
    save_sites(SITES)
    print(f"[REMOVED] {url}")
    return jsonify({'sites': SITES})

@app.route('/dashboard')
def dashboard():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MOM DETECTOR // CONTROL</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  :root {
    --red: #ff0033;
    --red-dim: #99001f;
    --red-glow: rgba(255,0,51,0.4);
    --bg: #080808;
    --bg2: #0f0f0f;
    --bg3: #141414;
    --border: #1f1f1f;
    --text: #e0e0e0;
    --text-dim: #555;
    --font-head: 'Orbitron', monospace;
    --font-mono: 'Share Tech Mono', monospace;
  }

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-mono);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    overflow-x: hidden;
  }

  /* scanline overlay */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,0,0,0.15) 2px,
      rgba(0,0,0,0.15) 4px
    );
    pointer-events: none;
    z-index: 100;
  }

  .panel {
    width: 100%;
    max-width: 520px;
    border: 1px solid var(--red-dim);
    background: var(--bg2);
    box-shadow: 0 0 40px var(--red-glow), inset 0 0 60px rgba(255,0,51,0.03);
    position: relative;
  }

  /* corner brackets */
  .panel::before, .panel::after {
    content: '';
    position: absolute;
    width: 16px;
    height: 16px;
    border-color: var(--red);
    border-style: solid;
  }
  .panel::before { top: -2px; left: -2px; border-width: 2px 0 0 2px; }
  .panel::after  { bottom: -2px; right: -2px; border-width: 0 2px 2px 0; }

  /* header */
  .header {
    border-bottom: 1px solid var(--border);
    padding: 24px 28px 20px;
    position: relative;
  }

  .header::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 60%;
    height: 1px;
    background: var(--red);
    box-shadow: 0 0 8px var(--red);
  }

  .header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
  }

  h1 {
    font-family: var(--font-head);
    font-size: 20px;
    font-weight: 900;
    letter-spacing: 0.15em;
    color: var(--red);
    text-shadow: 0 0 20px var(--red-glow);
  }

  .badge {
    font-size: 10px;
    letter-spacing: 0.2em;
    color: var(--text-dim);
    font-family: var(--font-mono);
  }

  /* status row */
  .status-row {
    padding: 20px 28px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .status-left {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--text-dim);
    transition: all 0.3s;
    flex-shrink: 0;
  }
  .dot.on {
    background: var(--red);
    box-shadow: 0 0 12px var(--red), 0 0 24px var(--red-glow);
  }

  .status-label {
    font-family: var(--font-head);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: var(--text-dim);
    transition: color 0.3s;
  }
  .status-label.on { color: var(--red); text-shadow: 0 0 12px var(--red-glow); }

  /* toggle */
  .toggle {
    width: 56px;
    height: 28px;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 14px;
    cursor: pointer;
    position: relative;
    transition: all 0.3s;
    flex-shrink: 0;
  }
  .toggle.on {
    background: rgba(255,0,51,0.15);
    border-color: var(--red-dim);
    box-shadow: 0 0 12px var(--red-glow);
  }
  .toggle-knob {
    position: absolute;
    top: 3px; left: 3px;
    width: 20px; height: 20px;
    background: #333;
    border-radius: 50%;
    transition: all 0.3s;
  }
  .toggle.on .toggle-knob {
    left: 31px;
    background: var(--red);
    box-shadow: 0 0 8px var(--red);
  }

  /* body */
  .body {
    padding: 24px 28px;
  }

  .section-label {
    font-family: var(--font-head);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.25em;
    color: var(--text-dim);
    margin-bottom: 14px;
  }

  /* add input */
  .add-row {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
  }

  .add-row input {
    flex: 1;
    background: var(--bg);
    border: 1px solid #222;
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 13px;
    padding: 10px 14px;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .add-row input::placeholder { color: var(--text-dim); }
  .add-row input:focus {
    border-color: var(--red-dim);
    box-shadow: 0 0 8px var(--red-glow);
  }

  .btn-add {
    background: var(--red);
    border: none;
    color: #fff;
    font-family: var(--font-head);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 10px 16px;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }
  .btn-add:hover {
    background: #ff2244;
    box-shadow: 0 0 16px var(--red-glow);
  }
  .btn-add:active { transform: scale(0.97); }

  /* site list */
  .sites-list {
    border: 1px solid var(--border);
    background: var(--bg);
    max-height: 320px;
    overflow-y: auto;
  }

  .site-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 11px 14px;
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
    gap: 12px;
  }
  .site-item:last-child { border-bottom: none; }
  .site-item:hover { background: #111; }

  .site-url {
    font-family: var(--font-mono);
    font-size: 12px;
    color: #888;
    word-break: break-all;
    flex: 1;
    transition: color 0.2s;
  }
  .site-item:hover .site-url { color: var(--text); }

  .btn-remove {
    background: transparent;
    border: 1px solid #2a2a2a;
    color: var(--text-dim);
    font-family: var(--font-mono);
    font-size: 11px;
    padding: 4px 10px;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .btn-remove:hover {
    border-color: var(--red);
    color: var(--red);
    box-shadow: 0 0 8px var(--red-glow);
  }

  .empty {
    padding: 32px;
    text-align: center;
    color: var(--text-dim);
    font-size: 12px;
    letter-spacing: 0.1em;
  }

  /* footer */
  .footer {
    padding: 14px 28px;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .site-count {
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 0.1em;
  }

  .site-count span { color: var(--red); }

  /* scrollbar */
  .sites-list::-webkit-scrollbar { width: 4px; }
  .sites-list::-webkit-scrollbar-track { background: transparent; }
  .sites-list::-webkit-scrollbar-thumb { background: #2a2a2a; }
  .sites-list::-webkit-scrollbar-thumb:hover { background: var(--red-dim); }
</style>
</head>
<body>

<div class="panel">
  <div class="header">
    <div class="header-top">
      <h1>MOM DETECTOR</h1>
      <span class="badge">PORT 5555</span>
    </div>
    <div class="badge">CONTROL PANEL // v2.0</div>
  </div>

  <div class="status-row">
    <div class="status-left">
      <div class="dot on" id="dot"></div>
      <span class="status-label on" id="statusLabel">ACTIVE</span>
    </div>
    <div class="toggle on" id="toggle">
      <div class="toggle-knob"></div>
    </div>
  </div>

  <div class="body">
    <div class="section-label">DECOY SITES</div>

    <div class="add-row">
      <input type="text" id="urlInput" placeholder="https://example.com">
      <button class="btn-add" id="addBtn">+ ADD</button>
    </div>

    <div class="sites-list" id="sitesList">
      <div class="empty">LOADING...</div>
    </div>
  </div>

  <div class="footer">
    <span class="site-count">SITES: <span id="count">0</span></span>
    <span class="site-count" id="triggerStatus"></span>
  </div>
</div>

<script>
  const toggle = document.getElementById('toggle');
  const dot = document.getElementById('dot');
  const statusLabel = document.getElementById('statusLabel');
  const sitesList = document.getElementById('sitesList');
  const urlInput = document.getElementById('urlInput');
  const addBtn = document.getElementById('addBtn');
  const countEl = document.getElementById('count');
  const triggerStatus = document.getElementById('triggerStatus');

  let enabled = true;

  function setStatus(on) {
    enabled = on;
    if (on) {
      toggle.classList.add('on');
      dot.classList.add('on');
      statusLabel.classList.add('on');
      statusLabel.textContent = 'ACTIVE';
      triggerStatus.textContent = '';
    } else {
      toggle.classList.remove('on');
      dot.classList.remove('on');
      statusLabel.classList.remove('on');
      statusLabel.textContent = 'DISABLED';
      triggerStatus.textContent = 'TRIGGERS BLOCKED';
    }
  }

  function renderSites(sites) {
    countEl.textContent = sites.length;
    if (sites.length === 0) {
      sitesList.innerHTML = '<div class="empty">NO SITES — ADD ONE ABOVE</div>';
      return;
    }
    sitesList.innerHTML = sites.map(site => `
      <div class="site-item">
        <span class="site-url">${site}</span>
        <button class="btn-remove" onclick="removeSite('${site.replace(/'/g, "\\'")}')">REMOVE</button>
      </div>
    `).join('');
  }

  async function loadStatus() {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      setStatus(data.enabled);
      renderSites(data.sites);
    } catch(e) {
      sitesList.innerHTML = '<div class="empty">ERROR CONNECTING TO SERVER</div>';
    }
  }

  toggle.addEventListener('click', async () => {
    try {
      const res = await fetch('/api/toggle', { method: 'POST' });
      const data = await res.json();
      setStatus(data.enabled);
    } catch(e) { console.error(e); }
  });

  addBtn.addEventListener('click', addSite);
  urlInput.addEventListener('keypress', e => { if (e.key === 'Enter') addSite(); });

  async function addSite() {
    const url = urlInput.value.trim();
    if (!url) return;
    try {
      const res = await fetch('/api/add-site', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      if (res.ok) {
        const data = await res.json();
        renderSites(data.sites);
        urlInput.value = '';
      } else {
        const err = await res.json();
        alert(err.error);
      }
    } catch(e) { console.error(e); }
  }

  async function removeSite(url) {
    try {
      const res = await fetch('/api/remove-site', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      if (res.ok) {
        const data = await res.json();
        renderSites(data.sites);
      }
    } catch(e) { console.error(e); }
  }

  loadStatus();
</script>
</body>
</html>'''

if __name__ == '__main__':
    print("Mom Detector running on port 5555...")
    print("Dashboard -> http://localhost:5555/dashboard")
    app.run(host='0.0.0.0', port=5555)
