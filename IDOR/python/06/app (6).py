from flask import Flask, request, render_template_string, jsonify, redirect, url_for

app = Flask(__name__)

MESSAGES = {
    1:  {"id": 1,  "owner_id": 101, "from": "system",  "subject": "Welcome to MsgBox!",          "body": "Thanks for signing up. Enjoy the platform.", "read": True},
    2:  {"id": 2,  "owner_id": 101, "from": "bob",     "subject": "Hey Alice!",                   "body": "Did you see the game last night?",            "read": False},
    3:  {"id": 3,  "owner_id": 102, "from": "system",  "subject": "Your password was changed",    "body": "If this wasn't you, contact support.",        "read": False},
    4:  {"id": 4,  "owner_id": 100, "from": "system",  "subject": "Admin Alert — Credentials",   "body": "FLAG{idor_level_6_delete_another_user_message}", "read": False},
}

CURRENT_USER_ID = 101
CURRENT_USER = "alice"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MsgBox — Inbox</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #f1f5f9; --white: #fff; --border: #e2e8f0;
            --ink: #0f172a; --muted: #64748b; --accent: #6366f1; --accent-light: #eef2ff; --danger: #ef4444;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 1px solid var(--border); padding: 0 40px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 17px; }
        .nav-logo span { color: var(--accent); }
        .nav-user { font-size: 13px; color: var(--muted); }
        .container { max-width: 760px; margin: 0 auto; padding: 40px 24px; }
        h1 { font-size: 22px; font-weight: 700; margin-bottom: 24px; }
        .msg-card { background: var(--white); border: 1px solid var(--border); border-radius: 8px; padding: 16px 20px; margin-bottom: 10px; display: flex; align-items: center; gap: 14px; transition: box-shadow 0.15s; }
        .msg-card:hover { box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
        .msg-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); flex-shrink: 0; }
        .msg-dot.read { background: transparent; border: 1px solid var(--border); }
        .msg-body { flex: 1; }
        .msg-from { font-size: 13px; color: var(--muted); margin-bottom: 2px; }
        .msg-subject { font-size: 15px; font-weight: 600; }
        .msg-actions { display: flex; gap: 8px; }
        .read-btn { padding: 6px 12px; border: 1px solid var(--border); border-radius: 5px; background: var(--white); font-size: 12px; font-weight: 500; cursor: pointer; }
        .read-btn:hover { background: var(--bg); }
        .del-btn { padding: 6px 12px; border: 1px solid #fecaca; border-radius: 5px; background: #fff5f5; color: var(--danger); font-size: 12px; font-weight: 500; cursor: pointer; }
        .del-btn:hover { background: #fee2e2; }
        #msg-detail { margin-top: 24px; background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 24px; display: none; }
        #msg-detail h3 { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
        #msg-detail .from { font-size: 13px; color: var(--muted); margin-bottom: 14px; }
        #msg-detail .body-text { font-size: 15px; line-height: 1.7; }
    </style>
</head>
<body>
<nav>
    <div class="nav-logo">Msg<span>Box</span></div>
    <div class="nav-user">{{ current_user }}</div>
</nav>
<div class="container">
    <h1>Inbox</h1>
    {% for msg in messages %}
    <div class="msg-card" id="msg-{{ msg.id }}">
        <div class="msg-dot {{ 'read' if msg.read else '' }}"></div>
        <div class="msg-body">
            <div class="msg-from">From: {{ msg.from }}</div>
            <div class="msg-subject">{{ msg.subject }}</div>
        </div>
        <div class="msg-actions">
            <button class="read-btn" onclick="readMsg({{ msg.id }})">Read</button>
            <button class="del-btn" onclick="deleteMsg({{ msg.id }})">Delete</button>
        </div>
    </div>
    {% endfor %}

    <div id="msg-detail">
        <h3 id="detail-subject"></h3>
        <div id="detail-from" class="from"></div>
        <div id="detail-body" class="body-text"></div>
    </div>
</div>
<script>
function readMsg(msgId) {
    fetch('/api/message?id=' + msgId)
        .then(r => r.json())
        .then(data => {
            document.getElementById('msg-detail').style.display = 'block';
            document.getElementById('detail-subject').textContent = data.subject || data.error;
            document.getElementById('detail-from').textContent = 'From: ' + (data.from || '');
            document.getElementById('detail-body').textContent = data.body || '';
        });
}

function deleteMsg(msgId) {
    fetch('/api/delete', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message_id: msgId})
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            document.getElementById('msg-' + msgId).style.display = 'none';
        }
        alert(data.message || data.error);
    });
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    my_msgs = [m for m in MESSAGES.values() if m["owner_id"] == CURRENT_USER_ID]
    return render_template_string(HTML, messages=my_msgs, current_user=CURRENT_USER)

@app.route("/api/message")
def api_message():
    msg_id = request.args.get("id", type=int)
    msg = MESSAGES.get(msg_id)
    if not msg:
        return jsonify({"error": "Message not found"}), 404
    # No ownership check
    return jsonify(msg)

@app.route("/api/delete", methods=["POST"])
def api_delete():
    data = request.get_json()
    msg_id = data.get("message_id")
    msg = MESSAGES.get(msg_id)
    if not msg:
        return jsonify({"error": "Message not found"}), 404
    # No ownership check — deletes any message
    del MESSAGES[msg_id]
    return jsonify({"success": True, "message": f"Message {msg_id} deleted."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
