from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

INVOICES = {
    "INV-1001": {"id": "INV-1001", "owner": "alice", "owner_id": 101, "amount": "$249.00", "status": "Paid",    "date": "2024-03-01", "items": ["Pro Plan x1", "Add-on Pack x2"]},
    "INV-1002": {"id": "INV-1002", "owner": "alice", "owner_id": 101, "amount": "$49.00",  "status": "Pending", "date": "2024-03-15", "items": ["Pro Plan x1"]},
    "INV-1003": {"id": "INV-1003", "owner": "bob",   "owner_id": 102, "amount": "$749.00", "status": "Paid",    "date": "2024-02-28", "items": ["Enterprise Plan x1"]},
    "INV-1004": {"id": "INV-1004", "owner": "admin", "owner_id": 100, "amount": "$0.00",   "status": "Internal","date": "2024-01-01", "items": ["Internal Invoice — FLAG{idor_level_5_invoice_id_guessing}"]},
}

CURRENT_USER = "alice"
CURRENT_USER_ID = 101

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BillDesk — Invoices</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #fafafa; --white: #fff; --border: #e5e7eb;
            --ink: #111827; --muted: #6b7280; --accent: #059669; --accent-light: #ecfdf5;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 1px solid var(--border); padding: 0 40px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 17px; }
        .nav-logo span { color: var(--accent); }
        .nav-user { font-size: 13px; color: var(--muted); }
        .container { max-width: 800px; margin: 0 auto; padding: 40px 24px; }
        h1 { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
        .sub { color: var(--muted); font-size: 14px; margin-bottom: 28px; }
        .inv-card { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 18px 22px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; }
        .inv-id { font-size: 13px; font-weight: 700; color: var(--accent); font-family: monospace; }
        .inv-date { font-size: 13px; color: var(--muted); }
        .inv-amount { font-size: 16px; font-weight: 700; }
        .inv-status { font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
        .status-paid { background: var(--accent-light); color: var(--accent); }
        .status-pending { background: #fef9c3; color: #854d0e; }
        .view-btn { padding: 7px 16px; border: 1px solid var(--border); border-radius: 6px; background: var(--white); font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500; cursor: pointer; }
        .view-btn:hover { background: var(--bg); }
        #invoice-detail { margin-top: 28px; background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 24px; display: none; }
        #invoice-detail h3 { font-size: 16px; font-weight: 700; margin-bottom: 16px; }
        .d-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 14px; }
        .d-row:last-child { border-bottom: none; }
        .d-label { color: var(--muted); }
    </style>
</head>
<body>
<nav>
    <div class="nav-logo">Bill<span>Desk</span></div>
    <div class="nav-user">{{ current_user }}</div>
</nav>
<div class="container">
    <h1>My Invoices</h1>
    <p class="sub">Your billing history and payment records.</p>

    {% for inv in invoices %}
    <div class="inv-card">
        <div>
            <div class="inv-id">{{ inv.id }}</div>
            <div class="inv-date">{{ inv.date }}</div>
        </div>
        <div class="inv-amount">{{ inv.amount }}</div>
        <span class="inv-status status-{{ inv.status.lower() }}">{{ inv.status }}</span>
        <button class="view-btn" onclick="viewInvoice('{{ inv.id }}')">View</button>
    </div>
    {% endfor %}

    <div id="invoice-detail">
        <h3 id="inv-title">Invoice Detail</h3>
        <div id="inv-rows"></div>
    </div>
</div>
<script>
function viewInvoice(invId) {
    fetch('/api/invoice?id=' + invId)
        .then(r => r.json())
        .then(data => {
            const detail = document.getElementById('invoice-detail');
            detail.style.display = 'block';
            document.getElementById('inv-title').textContent = 'Invoice ' + (data.id || '');
            const rows = document.getElementById('inv-rows');
            rows.innerHTML = '';
            for (const [k, v] of Object.entries(data)) {
                const row = document.createElement('div');
                row.className = 'd-row';
                row.innerHTML = '<span class="d-label">' + k + '</span><span>' + (Array.isArray(v) ? v.join(', ') : v) + '</span>';
                rows.appendChild(row);
            }
        });
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    my_invoices = [i for i in INVOICES.values() if i["owner_id"] == CURRENT_USER_ID]
    return render_template_string(HTML, invoices=my_invoices, current_user=CURRENT_USER)

@app.route("/api/invoice")
def api_invoice():
    inv_id = request.args.get("id", "")
    inv = INVOICES.get(inv_id)
    if not inv:
        return jsonify({"error": "Invoice not found"}), 404
    # No ownership check
    return jsonify(inv)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
