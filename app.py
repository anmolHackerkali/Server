from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_KEY = "KEY_344C3EE8_WEBCYBER"
API_URL = "https://anishexploits.com/api/api.php"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 Number Details Checker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body {
            background: linear-gradient(145deg, #0d0d0d 0%, #1a1a2e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(20, 20, 40, 0.95);
            backdrop-filter: blur(12px);
            width: 100%;
            max-width: 580px;
            border-radius: 24px;
            padding: 35px 30px 40px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        }
        h1 {
            text-align: center;
            font-weight: 600;
            font-size: 26px;
            color: #e0e0ff;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        .sub {
            text-align: center;
            color: #8888aa;
            font-size: 14px;
            margin-bottom: 28px;
        }
        .sub span { color: #7aa2f7; font-weight: 600; }
        form {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        label {
            color: #b0b0d0;
            font-size: 14px;
            font-weight: 500;
        }
        input[type="text"] {
            width: 100%;
            padding: 14px 18px;
            border-radius: 12px;
            border: 1px solid #333355;
            background: #12121e;
            color: #f0f0ff;
            font-size: 18px;
            letter-spacing: 1px;
            outline: none;
            transition: 0.25s;
        }
        input[type="text"]:focus {
            border-color: #7aa2f7;
            box-shadow: 0 0 0 3px rgba(122,162,247,0.15);
        }
        button {
            padding: 14px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, #7aa2f7, #3b82f6);
            color: #fff;
            font-size: 17px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.25s;
            letter-spacing: 0.5px;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(122,162,247,0.35); }
        button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

        .result-box {
            margin-top: 25px;
            background: #0d0d18;
            border-radius: 16px;
            padding: 20px;
            border: 1px solid #2a2a4a;
        }
        .result-box h3 {
            color: #7aa2f7;
            font-size: 15px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 14px;
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .detail-row:last-child { border-bottom: none; }
        .detail-label { color: #8888aa; font-size: 14px; }
        .detail-value { color: #e0e0ff; font-size: 14px; font-weight: 500; text-align: right; max-width: 60%; word-break: break-word; }

        .error {
            margin-top: 20px;
            background: rgba(255,70,70,0.12);
            border: 1px solid rgba(255,70,70,0.3);
            border-radius: 12px;
            padding: 14px 18px;
            color: #ff6b6b;
            font-size: 14px;
            text-align: center;
        }
        .footer {
            text-align: center;
            margin-top: 22px;
            font-size: 12px;
            color: #555577;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Number Lookup</h1>
        <div class="sub">API by <span>@Hello Hacker's</span></div>

        <form method="POST">
            <label for="phone">📞 Mobile Number (10 अंक)</label>
            <input type="text" id="phone" name="phone" placeholder="9876543210" value="{{ phone or '' }}" required maxlength="10" pattern="[0-9]{10}">
            <button type="submit" id="submitBtn">➤ Details निकालें</button>
        </form>

        {% if result %}
        <div class="result-box">
            <h3>✅ Result — {{ num }}</h3>
            {% for r in result %}
            <div class="detail-row">
                <span class="detail-label">नाम</span>
                <span class="detail-value">{{ r.name }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">पिता का नाम</span>
                <span class="detail-value">{{ r.fname }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">पता</span>
                <span class="detail-value">{{ r.address }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">आधार</span>
                <span class="detail-value">{{ r.aadhar }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Alt Number</span>
                <span class="detail-value">{{ r.alt }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Operator</span>
                <span class="detail-value">{{ r.circle }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Email</span>
                <span class="detail-value">{{ r.email or '❌ नहीं मिला' }}</span>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% if error %}
        <div class="error">⚠️ {{ error }}</div>
        {% endif %}

        <div class="footer">Powered by PyAura 🔥</div>
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

        # Input validation
        if not phone or not phone.isdigit() or len(phone) != 10:
            error = "❌ कृपया सिर्फ 10 अंकों का मोबाइल नंबर डालें (जैसे → 9876543210)"
        else:
            try:
                params = {
                    'key': API_KEY,
                    'type': 'number',
                    'num': phone
                }
                resp = requests.get(API_URL, params=params, timeout=15)
                data = resp.json()

                if data.get('status') == 'success' and data.get('result'):
                    result = data['result']
                else:
                    error = "⚠️ API से कोई डेटा नहीं मिला। नंबर सही है? या API key वैलिड है?"
            except requests.exceptions.Timeout:
                error = "⏱️ API ने समय सीमा में रिस्पॉन्स नहीं दिया। बाद में प्रयास करें।"
            except requests.exceptions.ConnectionError:
                error = "🔌 API से कनेक्शन नहीं हो पाया। इंटरनेट चेक करें।"
            except Exception as e:
                error = f"❌ त्रुटि: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result, error=error, phone=phone, num=phone)

if __name__ == '__main__':
    print("🔥 PyAura Number Checker चालू हो गया!")
    print("👉 http://127.0.0.1:5000 पर खुलेगा")
    app.run(debug=True, host='0.0.0.0', port=5000)
