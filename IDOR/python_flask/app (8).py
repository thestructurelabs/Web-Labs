from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

PUBLIC_USERS = {
    "alice-2024": {"slug": "alice-2024", "user_id": 101, "display_name": "Alice K.", "bio": "Designer & creator"},
    "bob-dev":    {"slug": "bob-dev",    "user_id": 102, "display_name": "Bob T.",   "bio": "Backend engineer"},
    "carol-art":  {"slug": "carol-art",  "user_id": 103, "display_name": "Carol M.", "bio": "Illustrator"},
}

PRIVATE_DATA = {
    101: {"user_id": 101, "email": "alice@example.com",  "phone": "+1-555-0101", "address": "12 Maple St"},
    102: {"user_id": 102, "email": "bob@example.com",    "phone": "+1-555-0102", "address": "88 Oak Ave"},
    103: {"user_id": 103, "email": "carol@example.com",  "phone": "+1-555-0103", "address": "5 Pine Rd"},
    100: {"user_id": 100, "email": "admin@platform.io",  "phone": "+1-555-0000", "address": "HQ Building", "flag": "FLAG{idor_level_8_chained_slug_to_id}"},
}

PUBLIC_USERS["admin-sys"] = {"slug": "admin-sys", "user_id": 100, "display_name": "Admin", "bio": "System account"}

CURRENT_USER = "alice-2024"
CURRENT_USER_ID = 101

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CreatorHub — Profiles</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #faf9f7; --white: #fff; --border: #e7e5e0;
            --ink: #1c1917; --muted: #78716c; --accent: #ea580c; --accent-light: #fff7ed;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 1px solid var(--border); padding: 0 40px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 17px; }
        .nav-logo span { color: var(--accent); }
        .nav-user { font-size: 13px; color: var(--muted); }
        .container { max-width: 800px; margin: 0 auto; padding: 40px 24px; }
        h1 { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
        .sub { color: var(--muted); font-size: 14px; margin-bottom: 28px; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 36px; }
        .user-card { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 20px; text-align: center; cursor: pointer; transition: box-shadow 0.15s; }
        .user-card:hover { box-shadow: 0 2px 10px rgba(0,0,0,0.07); }
        .uc-avatar { width: 48px; height: 48px; border-radius: 50%; background: var(--accent-light); color: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; margin: 0 auto 10px; }
        .uc-name { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
        .uc-bio { font-size: 12px; color: var(--muted); }
        .uc-slug { font-size: 11px; color: var(--accent); margin-top: 6px; font-family: monospace; }
        .api-section { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 24px; }
        .api-title { font-size: 14px; font-weight: 600; margin-bottom: 14px; }
        .api-row { display: flex; gap: 10px; margin-bottom: 10px; }
        .api-row input { flex: 1; padding: 10px 14px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; font-family: 'Inter', sans-serif; font-size: 14px; color: var(--ink); outline: none; }
        .api-row input:focus { border-color: var(--accent); }
        .api-row button { padding: 10px 18px; background: var(--accent); color: white; border: none; border-radius: 6px; font-weight: 600; font-size: 13px; cursor: pointer; }
        #result { margin-top: 14px; font-family: monospace; font-size: 13px; background: var(--bg); padding: 14px; border-radius: 6px; border: 1px solid var(--border); white-space: pre-wrap; display: none; }
        .endpoint-tag { font-family: monospace; font-size: 12px; color: var(--muted); margin-bottom: 8px; }
    </style>
</head>
<body>
<nav>
    <div class="nav-logo">Creator<span>Hub</span></div>
    <div class="nav-user">{{ current_user }}</div>
</nav>
<div class="container">
    <h1>Creator Directory</h1>
    <p class="sub">Browse public profiles on the platform.</p>

    <div class="grid">
        {% for slug, u in public_users.items() %}
        <div class="user-card" onclick="lookupSlug('{{ slug }}')">
            <div class="uc-avatar">{{ u.display_name[0] }}</div>
            <div class="uc-name">{{ u.display_name }}</div>
            <div class="uc-bio">{{ u.bio }}</div>
            <div class="uc-slug">@{{ slug }}</div>
        </div>
        {% endfor %}
    </div>

    <div class="api-section">
        <div class="api-title">Search Profiles</div>
        <div class="api-row">
            <input type="text" id="slug-input" placeholder="Enter username...">
            <button onclick="lookupSlug(document.getElementById('slug-input').value)">Search</button>
        </div>
        <div id="result"></div>
    </div>
</div>
<script>
function lookupSlug(slug) {
    document.getElementById('slug-input').value = slug;
    fetch('/api/user/slug?slug=' + encodeURIComponent(slug))
        .then(r => r.json())
        .then(data => showResult(data));
}
function lookupPrivate(userId) {
    fetch('/api/user/private?user_id=' + encodeURIComponent(userId))
        .then(r => r.json())
        .then(data => showResult(data));
}
function showResult(data) {
    const el = document.getElementById('result');
    el.style.display = 'block';
    el.textContent = JSON.stringify(data, null, 2);
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    visible = {k: v for k, v in PUBLIC_USERS.items() if k != "admin-sys"}
    return render_template_string(HTML, public_users=visible, current_user=CURRENT_USER)

@app.route("/api/user/slug")
def api_slug():
    slug = request.args.get("slug", "")
    user = PUBLIC_USERS.get(slug)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route("/api/user/private")
def api_private():
    user_id = request.args.get("user_id", type=int)
    data = PRIVATE_DATA.get(user_id)
    if not data:
        return jsonify({"error": "Not found"}), 404
    # No ownership check
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
