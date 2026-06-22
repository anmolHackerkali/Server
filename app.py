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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
            --text-primary: #e0e0ff;
            --text-dim: #6b6b8a;
            --glow-cyan: 0 0 10px rgba(0, 243, 255, 0.3), 0 0 40px rgba(0, 243, 255, 0.1);
            --glow-green: 0 0 10px rgba(0, 255, 65, 0.3), 0 0 40px rgba(0, 255, 65, 0.1);
            --glow-pink: 0 0 10px rgba(255, 0, 170, 0.3), 0 0 40px rgba(255, 0, 170, 0.1);
        }

        body {
            background: var(--dark-bg);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 16px;
            font-family: 'Share Tech Mono', monospace;
            position: relative;
            overflow-x: hidden;
        }

        /* Animated Matrix Rain Background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(0, 255, 65, 0.015) 2px,
                    rgba(0, 255, 65, 0.015) 4px
                );
            pointer-events: none;
            z-index: 0;
            animation: matrixScroll 20s linear infinite;
        }

        @keyframes matrixScroll {
            0% { transform: translateY(0); }
            100% { transform: translateY(-50px); }
        }

        /* Scanline overlay */
        body::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 3px,
                rgba(0, 0, 0, 0.03) 3px,
                rgba(0, 0, 0, 0.03) 6px
            );
            pointer-events: none;
            z-index: 1;
        }

        .container {
            position: relative;
            z-index: 2;
            background: var(--dark-card);
            width: 100%;
            max-width: 560px;
            border-radius: 16px;
            padding: 30px 24px 35px;
            border: 1px solid var(--dark-border);
            box-shadow:
                0 0 30px rgba(0, 243, 255, 0.05),
                inset 0 0 30px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            animation: containerPulse 4s ease-in-out infinite;
        }

        @keyframes containerPulse {
            0%, 100% { border-color: var(--dark-border); box-shadow: 0 0 30px rgba(0, 243, 255, 0.05); }
            50% { border-color: rgba(0, 243, 255, 0.15); box-shadow: 0 0 30px rgba(0, 243, 255, 0.1); }
        }

        /* Header with glitch effect */
        .header {
            text-align: center;
            margin-bottom: 8px;
            position: relative;
        }

        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0 14px 0;
            border-bottom: 1px solid rgba(0, 243, 255, 0.1);
            margin-bottom: 18px;
            font-size: 11px;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .status-bar .status-led {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .led {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            animation: blink 1.5s ease-in-out infinite;
        }

        .led.green { background: var(--neon-green); box-shadow: 0 0 6px var(--neon-green); }
        .led.cyan { background: var(--neon-cyan); box-shadow: 0 0 6px var(--neon-cyan); }
        .led.pink { background: var(--neon-pink); box-shadow: 0 0 6px var(--neon-pink); }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        .glitch-wrapper {
            position: relative;
            display: inline-block;
        }

        .glitch-title {
            font-family: 'Orbitron', monospace;
            font-weight: 900;
            font-size: clamp(18px, 5vw, 28px);
            color: var(--neon-cyan);
            text-shadow: var(--glow-cyan);
            letter-spacing: 3px;
            text-transform: uppercase;
            position: relative;
        }

        .glitch-title::before,
        .glitch-title::after {
            content: '● PHONE_LOOKUP v2.0 ●';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
        }

        .glitch-title::before {
            color: var(--neon-pink);
            z-index: -1;
            animation: glitch1 3s infinite;
        }

        .glitch-title::after {
            color: var(--neon-cyan);
            z-index: -1;
            animation: glitch2 3s infinite;
        }

        @keyframes glitch1 {
            0%, 90%, 100% { opacity: 0; transform: translate(0); }
            92% { opacity: 0.6; transform: translate(-2px, 1px); }
            94% { opacity: 0; transform: translate(0); }
            96% { opacity: 0.4; transform: translate(2px, -1px); }
            98% { opacity: 0; transform: translate(0); }
        }

        @keyframes glitch2 {
            0%, 85%, 100% { opacity: 0; transform: translate(0); }
            87% { opacity: 0.5; transform: translate(2px, -1px); }
            89% { opacity: 0; transform: translate(0); }
            91% { opacity: 0.3; transform: translate(-1px, 2px); }
            93% { opacity: 0; transform: translate(0); }
        }

        .sub {
            text-align: center;
            color: var(--text-dim);
            font-size: 12px;
            letter-spacing: 2px;
            margin-top: 6px;
            margin-bottom: 20px;
        }

        .sub .highlight {
            color: var(--neon-green);
            text-shadow: 0 0 8px rgba(0, 255, 65, 0.3);
            font-weight: 600;
        }

        /* Form */
        form {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .input-group {
            position: relative;
        }

        .input-group label {
            display: block;
            color: var(--text-dim);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 6px;
        }

        .input-group label .prompt {
            color: var(--neon-green);
        }

        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .input-wrapper .prefix {
            position: absolute;
            left: 16px;
            color: var(--neon-cyan);
            font-size: 16px;
            opacity: 0.6;
            font-family: 'Share Tech Mono', monospace;
            pointer-events: none;
            z-index: 2;
        }

        input[type="text"] {
            width: 100%;
            padding: 14px 18px 14px 42px;
            border-radius: 10px;
            border: 1px solid #1a1a3a;
            background: rgba(0, 0, 0, 0.6);
            color: var(--neon-green);
            font-family: 'Share Tech Mono', monospace;
            font-size: 20px;
            letter-spacing: 3px;
            outline: none;
            transition: all 0.3s ease;
        }

        input[type="text"]:focus {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.15), inset 0 0 15px rgba(0, 243, 255, 0.05);
            background: rgba(0, 0, 0, 0.8);
        }

        input[type="text"]::placeholder {
            color: #2a2a4a;
            letter-spacing: 1px;
            font-size: 14px;
        }

        /* Terminal typing effect on button */
        .btn-wrapper {
            position: relative;
            margin-top: 6px;
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
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            letter-spacing: 3px;
            text-transform: uppercase;
            border: 1px solid rgba(0, 243, 255, 0.2);
            position: relative;
            overflow: hidden;
        }

        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.1), transparent);
            transition: 0.5s;
        }

        button:hover::before {
            left: 100%;
        }

        button:hover {
            border-color: var(--neon-cyan);
            box-shadow: var(--glow-cyan), inset 0 0 20px rgba(0, 243, 255, 0.05);
            transform: translateY(-2px);
            background: linear-gradient(135deg, rgba(0, 243, 255, 0.2), rgba(0, 255, 65, 0.15));
        }

        button:active {
            transform: translateY(1px);
        }

        button:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none !important;
        }

        .btn-status {
            display: block;
            text-align: right;
            font-size: 10px;
            color: #2a2a4a;
            margin-top: 4px;
            letter-spacing: 1px;
        }

        /* Result Box - Hacker Terminal Style */
        .result-box {
            margin-top: 24px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 12px;
            padding: 0;
            border: 1px solid rgba(0, 255, 65, 0.15);
            overflow: hidden;
            animation: fadeInResult 0.5s ease-out;
        }

        @keyframes fadeInResult {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-header {
            background: rgba(0, 255, 65, 0.05);
            padding: 12px 18px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .result-header .title {
            color: var(--neon-green);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .result-header .target-num {
            color: var(--neon-cyan);
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 2px;
        }

        .result-body {
            padding: 6px 0;
        }

        .detail-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 18px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            transition: background 0.2s;
        }

        .detail-row:last-child { border-bottom: none; }
        .detail-row:hover { background: rgba(0, 243, 255, 0.03); }

        .detail-label {
            color: var(--text-dim);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .detail-label .arrow {
            color: var(--neon-cyan);
            opacity: 0.5;
        }

        .detail-value {
            color: var(--text-primary);
            font-size: 13px;
            text-align: right;
            max-width: 55%;
            word-break: break-word;
        }

        .detail-value.found {
            color: var(--neon-green);
            text-shadow: 0 0 8px rgba(0, 255, 65, 0.2);
        }

        .detail-value.not-found {
            color: #ff4444;
            opacity: 0.7;
        }

        /* Error Box */
        .error {
            margin-top: 20px;
            background: rgba(255, 0, 0, 0.08);
            border: 1px solid rgba(255, 0, 0, 0.25);
            border-radius: 10px;
            padding: 14px 18px;
            color: #ff4444;
            font-size: 13px;
            text-align: center;
            letter-spacing: 0.5px;
        }

        .error::before {
            content: '⚠ ERROR :: ';
            color: #ff6666;
            font-weight: 600;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 11px;
            color: #2a2a4a;
            letter-spacing: 2px;
        }

        .footer .brand {
            color: var(--neon-pink);
            text-shadow: 0 0 8px rgba(255, 0, 170, 0.2);
        }

        .footer .cursor-blink {
            display: inline-block;
            width: 8px;
            height: 14px;
            background: var(--neon-green);
            animation: cursorBlink 1s step-end infinite;
            vertical-align: middle;
            margin-left: 4px;
        }

        @keyframes cursorBlink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        /* Loading animation */
        .loading {
            display: inline-block;
            position: relative;
        }

        .loading::after {
            content: '...';
            animation: loadingDots 1.5s steps(3, end) infinite;
        }

        @keyframes loadingDots {
            0% { content: '.'; }
            33% { content: '..'; }
            66% { content: '...'; }
            100% { content: '.'; }
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 4px;
        }
        ::-webkit-scrollbar-track {
            background: var(--dark-bg);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--dark-border);
            border-radius: 2px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--neon-cyan);
        }

        /* Responsive */
        @media (max-width: 480px) {
            .container {
                padding: 20px 16px 25px;
                border-radius: 12px;
            }
            .glitch-title {
                font-size: 16px;
                letter-spacing: 1px;
            }
            input[type="text"] {
                font-size: 18px;
                padding: 12px 14px 12px 38px;
            }
            .detail-row {
                padding: 8px 14px;
                flex-direction: column;
                align-items: flex-start;
                gap: 2px;
            }
            .detail-value {
                text-align: left;
                max-width: 100%;
                width: 100%;
            }
            .status-bar {
                font-size: 9px;
                flex-wrap: wrap;
                gap: 4px;
            }
            button {
                font-size: 14px;
                padding: 14px;
                letter-spacing: 2px;
            }
            .result-header {
                flex-direction: column;
                gap: 4px;
                align-items: flex-start;
            }
        }

        @media (min-width: 768px) {
            .container {
                padding: 40px 35px 45px;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Status Bar -->
        <div class="status-bar">
            <div class="status-led">
                <span class="led green"></span>
                <span>SYSTEM_READY</span>
            </div>
            <div>
                <span class="led cyan" style="animation-delay: 0.5s;"></span>
                <span id="clock">00:00:00</span>
            </div>
            <div>
                <span class="led pink" style="animation-delay: 1s;"></span>
                <span>v2.0.1</span>
            </div>
        </div>

        <!-- Title with Glitch -->
        <div class="header">
            <div class="glitch-wrapper">
                <h1 class="glitch-title">● PHONE_LOOKUP v2.0 ●</h1>
            </div>
            <div class="sub">
                <span class="highlight">⦿</span> TARGETED_QUERY_ENGINE <span class="highlight">⦿</span><br>
                <span style="font-size:10px; opacity:0.5;">API :: @Cyb3rS0ldier :: SECURED_CONNECTION</span>
            </div>
        </div>

        <!-- Form -->
        <form method="POST" autocomplete="off">
            <div class="input-group">
                <label>
                    <span class="prompt">root@hacker:~$</span> ./query --target
                </label>
                <div class="input-wrapper">
                    <span class="prefix">+91</span>
                    <input type="text" id="phone" name="phone" placeholder="XXXXXXXXXX" value="{{ phone or '' }}" required maxlength="10" pattern="[0-9]{10}" inputmode="numeric">
                </div>
            </div>

            <div class="btn-wrapper">
                <button type="submit" id="submitBtn">
                    ⚡ EXECUTE_QUERY
                </button>
                <span class="btn-status">[ENTER] to submit // [ESC] to clear</span>
            </div>
        </form>

        <!-- Result -->
        {% if result %}
        <div class="result-box">
            <div class="result-header">
                <span class="title">⫸ QUERY_RESULT</span>
                <span class="target-num">+91 {{ num }}</span>
            </div>
            <div class="result-body">
                {% for r in result %}
                <div class="detail-row">
                    <span class="detail-label"><span class="arrow">▶</span> NAME</span>
                    <span class="detail-value found">{{ r.name }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label"><span class="arrow">▶</span> FATHER</span>
                    <span class="detail-value found">{{ r.fname }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label"><span class="arrow">▶</span> ADDRESS</span>
                    <span class="detail-value">{{ r.address }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label"><span class="arrow">▶</span> AADHAAR</span>
                    <span class="detail-value found">{{ r.aadhar }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label"><span class="arrow">▶</span> ALT_NUM</span>
                    <span class="detail-value">{{ r.alt }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label"><span class="arrow">▶</span> OPERATOR</span>
                    <span class="detail-value">{{ r.circle }}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label"><span class="arrow">▶</span> EMAIL</span>
                    <span class="detail-value {% if r.email %}found{% else %}not-found{% endif %}">{{ r.email or 'N/A' }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}

        <!-- Footer -->
        <div class="footer">
            <span class="brand">◆ PYAURA_OSINT_ENGINE ◆</span> &nbsp;//&nbsp; SESSION_ACTIVE
            <span class="cursor-blink"></span>
        </div>
    </div>

    <script>
        // Live clock
        function updateClock() {
            const now = new Date();
            const time = now.toTimeString().split(' ')[0];
            document.getElementById('clock').textContent = time;
        }
        updateClock();
        setInterval(updateClock, 1000);

        // Keyboard shortcut: Enter triggers submit (already default)
        // ESC clears input
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const input = document.getElementById('phone');
                input.value = '';
                input.focus();
            }
        });

        // Button loading state
        document.querySelector('form').addEventListener('submit', function(e) {
            const btn = document.getElementById('submitBtn');
            const input = document.getElementById('phone');
            if (input.value.length === 10) {
                btn.disabled = true;
                btn.textContent = '⏳ PROCESSING...';
                // Re-enable after 30s timeout as fallback
                setTimeout(() => {
                    btn.disabled = false;
                    btn.textContent = '⚡ EXECUTE_QUERY';
                }, 30000);
            }
        });

        // Auto-focus input on load
        window.addEventListener('load', function() {
            document.getElementById('phone').focus();
        });

        // Input validation
        document.getElementById('phone').addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);
        });
    </script>
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
            error = "कृपया सिर्फ 10 अंकों का मोबाइल नंबर डालें (जैसे 6209876775)"
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
                    error = "API से कोई डेटा नहीं मिला। नंबर सही है? या API key वैलिड है?"
            except requests.exceptions.Timeout:
                error = "API ने समय सीमा में रिस्पॉन्स नहीं दिया। बाद में प्रयास करें।"
            except requests.exceptions.ConnectionError:
                error = "API से कनेक्शन नहीं हो पाया। इंटरनेट चेक करें।"
            except Exception as e:
                error = f"त्रुटि: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result, error=error, phone=phone, num=phone)

if __name__ == '__main__':
    print("🔥 PyAura OSINT Engine v2.0 चालू हो गया!")
    print("👉 http://127.0.0.1:5000 पर खुलेगा")
    app.run(debug=True, host='0.0.0.0', port=5000)