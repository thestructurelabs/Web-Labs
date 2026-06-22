from flask import Flask, request, render_template_string, jsonify
import base64
import json

app = Flask(__name__)

USERS = {
    101: {"id": 101, "name": "alice",  "email": "alice@example.com",  "role": "user",  "balance": "$120.00"},
    102: {"id": 102, "name": "bob",    "email": "bob@example.com",    "role": "user",  "balance": "$340.00"},
    103: {"id": 103, "name": "carol",  "email": "carol@example.com",  "role": "user",  "balance": "$55.00"},
    100: {"id": 100, "name": "admin",  "email": "admin@corp.io",      "role": "admin", "balance": "$99,999.00", "flag": "FLAG{idor_level_7_jwt_claim_tampering}"},
}

def make_token(user_id):
    header = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload = base64.b64encode(json.dumps({"user_id": user_id, "role": "user"}).encode()).decode().rstrip("=")
    signature = "fakesignature"
    return f"{header}.{payload}.{signature}"

def decode_token(token):
    try:
        parts = token.split(".")
        payload = parts[1]
        padding = 4 - len(payload) % 4
        payload += "=" * padding
        return json.loads(base64.b64decode(payload))
    except Exception:
        return None

ALICE_TOKEN = make_token(101)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WalletApp — Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #09090b; --surface: #18181b; --border: #27272a;
            --text: #fafafa; --muted: #71717a; --accent: #facc15; --accent-dim: rgba(250,204,21,0.1);
        }
        body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; min-height: 100vh; padding: 60px 20px; }
        .container { max-width: 660px; margin: 0 auto; }
        .logo { font-size: 12px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); margin-bottom: 40px; }
        h1 { font-size: 28px; font-weight: 700; margin-bottom: 6px; }
        .sub { color: var(--muted); font-size: 14px; margin-bottom: 36px; }
        .wallet-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 28px; margin-bottom: 20px; }
        .wallet-label { font-size: 12px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; }
        .wallet-balance { font-size: 36px; font-weight: 700; color: var(--accent); margin-bottom: 6px; }
        .wallet-user { font-size: 14px; color: var(--muted); }
        .token-box { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin-bottom: 20px; }
        .token-label { font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 10px; letter-spacing: 0.06em; text-transform: uppercase; }
        .token-value { font-family: monospace; font-size: 12px; color: var(--muted); word-break: break-all; background: var(--bg); padding: 10px 12px; border-radius: 6px; border: 1px solid var(--border); }
        .api-box { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 20px; }
        .api-label { font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 12px; letter-spacing: 0.06em; text-transform: uppercase; }
        .input-row { display: flex; gap: 10px; }
        .input-row input { flex: 1; padding: 10px 14px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; font-family: monospace; font-size: 12px; color: var(--text); outline: none; }
        .input-row input:focus { border-color: var(--accent); }
        .input-row button { padding: 10px 20px; background: var(--accent); color: var(--bg); border: none; border-radius: 6px; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 13px; cursor: pointer; }
        #api-result { margin-top: 14px; font-family: monospace; font-size: 13px; color: var(--text); background: var(--bg); padding: 14px; border-radius: 6px; border: 1px solid var(--border); white-space: pre-wrap; display: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">WalletApp · v3</div>
    <h1>My Dashboard</h1>
    <p class="sub">Logged in as <strong>alice</strong></p>

    <div class="wallet-card">
        <div class="wallet-label">Current Balance</div>
        <div class="wallet-balance" id="balance">$120.00</div>
        <div class="wallet-user">alice · user #101</div>
    </div>

    <div class="token-box">
        <div class="token-label">Your Session Token (JWT)</div>
        <div class="token-value" id="token-display">{{ token }}</div>
    </div>

    <div class="api-box">
        <div class="api-label">API — Load Account by Token</div>
        <div class="input-row">
            <input type="text" id="token-input" value="{{ token }}" placeholder="Paste JWT token...">
            <button onclick="loadAccount()">Fetch</button>
        </div>
        <div id="api-result"></div>
    </div>
</div>
<script>
function loadAccount() {
    const token = document.getElementById('token-input').value;
    fetch('/api/account', {
        headers: { 'Authorization': 'Bearer ' + token }
    })
    .then(r => r.json())
    .then(data => {
        const el = document.getElementById('api-result');
        el.style.display = 'block';
        el.textContent = JSON.stringify(data, null, 2);
    });
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, token=ALICE_TOKEN)

@app.route("/api/account")
def api_account():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "No token"}), 401
    token = auth[7:]
    claims = decode_token(token)
    if not claims:
        return jsonify({"error": "Invalid token"}), 401
    # Trusts user_id from token payload without verifying signature
    user_id = claims.get("user_id")
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
