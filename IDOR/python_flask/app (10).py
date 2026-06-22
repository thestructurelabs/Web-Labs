from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

PUBLIC_TICKETS = {
    "TKT-4481": {"id": "TKT-4481", "status": "Resolved",    "category": "Billing",  "owner_id": 101},
    "TKT-4482": {"id": "TKT-4482", "status": "In Progress", "category": "Technical","owner_id": 101},
    "TKT-4483": {"id": "TKT-4483", "status": "Open",        "category": "General",  "owner_id": 102},
    "TKT-4484": {"id": "TKT-4484", "status": "Resolved",    "category": "Security", "owner_id": 100},
}

FULL_TICKETS = {
    "TKT-4481": {"id": "TKT-4481", "owner_id": 101, "subject": "Overcharged on last invoice", "messages": ["User: I was billed twice for March.", "Support: Confirmed. Refund issued."]},
    "TKT-4482": {"id": "TKT-4482", "owner_id": 101, "subject": "Login not working on mobile",  "messages": ["User: Can't log in on iPhone.", "Support: Investigating."]},
    "TKT-4483": {"id": "TKT-4483", "owner_id": 102, "subject": "How do I cancel my account?", "messages": ["User: Please advise.", "Support: See cancellation guide."]},
    "TKT-4484": {"id": "TKT-4484", "owner_id": 100, "subject": "[INTERNAL] Security audit findings", "messages": [
        "Admin: Audit complete. Summary below.",
        "Admin: FLAG{idor_level_10_chained_ticket_enumeration}",
        "Admin: Do not share outside security team."
    ]},
}

CURRENT_USER_ID = 101
CURRENT_USER = "alice"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SupportDesk — My Tickets</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #f8fafc; --white: #fff; --border: #e2e8f0;
            --ink: #0f172a; --muted: #64748b; --accent: #8b5cf6; --accent-light: #f5f3ff;
            --green: #059669; --yellow: #d97706;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 1px solid var(--border); padding: 0 40px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 17px; }
        .nav-logo span { color: var(--accent); }
        .nav-user { font-size: 13px; color: var(--muted); }
        .layout { max-width: 900px; margin: 0 auto; padding: 40px 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        .section-title { font-size: 15px; font-weight: 700; margin-bottom: 16px; }
        .ticket-row { background: var(--white); border: 1px solid var(--border); border-radius: 8px; padding: 14px 18px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; cursor: pointer; transition: box-shadow 0.15s; }
        .ticket-row:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .ticket-id { font-family: monospace; font-size: 13px; font-weight: 600; color: var(--accent); }
        .ticket-cat { font-size: 12px; color: var(--muted); margin-top: 2px; }
        .status-badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 20px; }
        .status-resolved { background: #dcfce7; color: var(--green); }
        .status-in-progress { background: #fef9c3; color: var(--yellow); }
        .status-open { background: var(--accent-light); color: var(--accent); }
        .detail-panel { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 22px; }
        .detail-panel h3 { font-size: 14px; font-weight: 600; margin-bottom: 14px; }
        .field { margin-bottom: 12px; }
        .field label { display: block; font-size: 11px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin-bottom: 5px; }
        .field input { width: 100%; padding: 9px 12px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; font-family: monospace; font-size: 13px; color: var(--ink); outline: none; }
        .field input:focus { border-color: var(--accent); }
        .fetch-btn { width: 100%; padding: 10px; background: var(--accent); color: white; border: none; border-radius: 6px; font-weight: 700; font-size: 14px; cursor: pointer; }
        #ticket-result { margin-top: 14px; font-family: monospace; font-size: 12px; background: var(--bg); padding: 12px; border-radius: 6px; border: 1px solid var(--border); white-space: pre-wrap; display: none; max-height: 260px; overflow-y: auto; }
        .public-board { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 22px; }
    </style>
</head>
<body>
<nav>
    <div class="nav-logo">Support<span>Desk</span></div>
    <div class="nav-user">{{ current_user }}</div>
</nav>
<div class="layout">
    <div>
        <div class="public-board">
            <div class="section-title">📋 Public Ticket Status Board</div>
            <p style="font-size:13px;color:var(--muted);margin-bottom:14px">Live status for all open tickets.</p>
            {% for tid, t in all_tickets.items() %}
            <div class="ticket-row" onclick="selectTicket('{{ tid }}')">
                <div>
                    <div class="ticket-id">{{ tid }}</div>
                    <div class="ticket-cat">{{ t.category }}</div>
                </div>
                <span class="status-badge status-{{ t.status.lower().replace(' ', '-') }}">{{ t.status }}</span>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="detail-panel">
        <h3>Ticket Details</h3>
        <div class="field">
            <label>Ticket ID</label>
            <input type="text" id="ticket-id-input" placeholder="e.g. TKT-4481">
        </div>
        <button class="fetch-btn" onclick="fetchTicket()">View Details</button>
        <div id="ticket-result"></div>
    </div>
</div>
<script>
function selectTicket(id) {
    document.getElementById('ticket-id-input').value = id;
}
function fetchTicket() {
    const id = document.getElementById('ticket-id-input').value;
    fetch('/api/ticket?id=' + encodeURIComponent(id))
        .then(r => r.json())
        .then(data => {
            const el = document.getElementById('ticket-result');
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
    return render_template_string(HTML,
        all_tickets=PUBLIC_TICKETS,
        current_user=CURRENT_USER,
        current_user_id=CURRENT_USER_ID
    )

@app.route("/api/ticket")
def api_ticket():
    ticket_id = request.args.get("id", "")
    ticket = FULL_TICKETS.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify(ticket)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
