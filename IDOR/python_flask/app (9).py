from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

REPORTS = {
    101: {
        "user_id": 101, "name": "alice", "period": "Q1 2024",
        "revenue": "$12,400", "sessions": 1840, "conversions": 142,
        "top_source": "Organic Search"
    },
    102: {
        "user_id": 102, "name": "bob", "period": "Q1 2024",
        "revenue": "$8,200", "sessions": 970, "conversions": 88,
        "top_source": "Paid Ads"
    },
    103: {
        "user_id": 103, "name": "carol", "period": "Q1 2024",
        "revenue": "$31,000", "sessions": 5200, "conversions": 410,
        "top_source": "Referral"
    },
    100: {
        "user_id": 100, "name": "admin", "period": "Q1 2024",
        "revenue": "CLASSIFIED", "sessions": 0, "conversions": 0,
        "top_source": "N/A",
        "internal_note": "FLAG{idor_level_9_export_report_user_id}"
    },
}

CURRENT_USER_ID = 101
CURRENT_USER = "alice"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AnalyticsPro — Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #0a0a0a; --surface: #141414; --border: #222; 
            --text: #f5f5f5; --muted: #666; --accent: #22c55e; --accent-dim: rgba(34,197,94,0.1);
        }
        body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav { background: var(--surface); border-bottom: 1px solid var(--border); padding: 0 40px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 17px; }
        .nav-logo span { color: var(--accent); }
        .nav-user { font-size: 13px; color: var(--muted); }
        .container { max-width: 860px; margin: 0 auto; padding: 40px 24px; }
        h1 { font-size: 24px; font-weight: 700; margin-bottom: 6px; }
        .sub { color: var(--muted); font-size: 14px; margin-bottom: 32px; }
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 32px; }
        .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 20px; }
        .stat-label { font-size: 12px; font-weight: 600; color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
        .stat-value { font-size: 26px; font-weight: 700; color: var(--accent); }
        .stat-sub { font-size: 12px; color: var(--muted); margin-top: 4px; }
        .export-box { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 24px; }
        .export-title { font-size: 15px; font-weight: 600; margin-bottom: 14px; }
        .export-row { display: flex; gap: 10px; margin-bottom: 8px; align-items: center; }
        .export-row input { flex: 1; padding: 10px 14px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text); outline: none; }
        .export-row input:focus { border-color: var(--accent); }
        .export-row select { padding: 10px 14px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text); outline: none; }
        .export-btn { padding: 10px 22px; background: var(--accent); color: var(--bg); border: none; border-radius: 6px; font-weight: 700; font-size: 14px; cursor: pointer; white-space: nowrap; }
        .export-note { font-size: 12px; color: var(--muted); margin-top: 6px; font-family: monospace; }
        #export-result { margin-top: 16px; font-family: monospace; font-size: 13px; background: var(--bg); padding: 16px; border-radius: 6px; border: 1px solid var(--border); white-space: pre-wrap; display: none; }
    </style>
</head>
<body>
<nav>
    <div class="nav-logo">Analytics<span>Pro</span></div>
    <div class="nav-user">{{ current_user }} · #{{ current_user_id }}</div>
</nav>
<div class="container">
    <h1>Analytics Dashboard</h1>
    <p class="sub">Your performance overview for Q1 2024.</p>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Revenue</div>
            <div class="stat-value">$12,400</div>
            <div class="stat-sub">+8% vs last quarter</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Sessions</div>
            <div class="stat-value">1,840</div>
            <div class="stat-sub">Unique visitors</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Conversions</div>
            <div class="stat-value">142</div>
            <div class="stat-sub">7.7% rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Top Source</div>
            <div class="stat-value" style="font-size:16px;margin-top:6px">Organic</div>
            <div class="stat-sub">Search traffic</div>
        </div>
    </div>

    <div class="export-box">
        <div class="export-title">Export Report</div>
        <div class="export-row">
            <input type="number" id="uid-input" value="{{ current_user_id }}" placeholder="User ID">
            <select id="format-select">
                <option>JSON</option>
                <option>CSV</option>
            </select>
            <button class="export-btn" onclick="exportReport()">Export</button>
        </div>
        <div id="export-result"></div>
    </div>
</div>
<script>
function exportReport() {
    const uid = document.getElementById('uid-input').value;
    const fmt = document.getElementById('format-select').value.toLowerCase();
    fetch('/api/export?user_id=' + uid + '&format=' + fmt)
        .then(r => r.json())
        .then(data => {
            const el = document.getElementById('export-result');
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
    return render_template_string(HTML, current_user=CURRENT_USER, current_user_id=CURRENT_USER_ID)

@app.route("/api/export")
def api_export():
    user_id = request.args.get("user_id", type=int)
    report = REPORTS.get(user_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    # No ownership check
    return jsonify(report)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
