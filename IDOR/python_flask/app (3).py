from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

PROFILES = {
    "alice": {"username": "alice", "bio": "Photography lover 📷", "posts": 42, "followers": 310, "private": False},
    "bob":   {"username": "bob",   "bio": "Just a dev 💻",        "posts": 17, "followers": 89,  "private": False},
    "carol": {"username": "carol", "bio": "Designer & maker 🎨",  "posts": 93, "followers": 1200,"private": True},
    "admin": {"username": "admin", "bio": "System administrator", "posts": 0,  "followers": 0,   "private": True, "api_key": "FLAG{idor_level_3_api_username_enumeration}"},
}

CURRENT_USER = "alice"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profileo — User Profiles</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #0f172a; --surface: #1e293b; --border: #334155;
            --text: #e2e8f0; --muted: #64748b; --accent: #38bdf8; --accent-dim: rgba(56,189,248,0.1);
        }
        body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; min-height: 100vh; padding: 60px 20px; }
        .container { max-width: 640px; margin: 0 auto; }
        .logo { font-size: 12px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); margin-bottom: 36px; }
        h1 { font-size: 28px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 6px; }
        .sub { color: var(--muted); font-size: 15px; margin-bottom: 36px; }
        .search-row { display: flex; gap: 10px; margin-bottom: 32px; }
        .search-row input {
            flex: 1; padding: 12px 16px; background: var(--surface); border: 1px solid var(--border);
            border-radius: 6px; font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text); outline: none;
        }
        .search-row input:focus { border-color: var(--accent); }
        .search-row button {
            padding: 12px 22px; background: var(--accent); color: var(--bg); border: none;
            border-radius: 6px; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 14px; cursor: pointer;
        }
        .profile-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 24px; margin-bottom: 16px; }
        .profile-top { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
        .avatar { width: 48px; height: 48px; border-radius: 50%; background: var(--accent-dim); border: 2px solid var(--accent); display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; color: var(--accent); }
        .profile-name { font-size: 16px; font-weight: 600; }
        .profile-handle { font-size: 13px; color: var(--muted); }
        .profile-bio { font-size: 14px; color: var(--muted); margin-bottom: 16px; }
        .stats { display: flex; gap: 24px; }
        .stat { text-align: center; }
        .stat-num { font-size: 16px; font-weight: 700; }
        .stat-label { font-size: 12px; color: var(--muted); }
        .api-note { margin-top: 32px; padding: 16px 20px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; font-size: 13px; color: var(--muted); font-family: monospace; }
        .api-note .endpoint { color: var(--accent); }
        #api-result { margin-top: 20px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; font-family: monospace; font-size: 13px; white-space: pre-wrap; color: var(--text); display: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">Profileo · v2</div>
    <h1>User Directory</h1>
    <p class="sub">Search and view public profiles.</p>

    <div class="search-row">
        <input type="text" id="username-input" placeholder="Enter username..." value="alice">
        <button onclick="loadProfile()">Load Profile</button>
    </div>

    <div id="profile-area">
        {% for username, p in profiles.items() %}
        {% if not p.private %}
        <div class="profile-card">
            <div class="profile-top">
                <div class="avatar">{{ p.username[0].upper() }}</div>
                <div>
                    <div class="profile-name">{{ p.username }}</div>
                    <div class="profile-handle">@{{ p.username }}</div>
                </div>
            </div>
            <div class="profile-bio">{{ p.bio }}</div>
            <div class="stats">
                <div class="stat"><div class="stat-num">{{ p.posts }}</div><div class="stat-label">Posts</div></div>
                <div class="stat"><div class="stat-num">{{ p.followers }}</div><div class="stat-label">Followers</div></div>
            </div>
        </div>
        {% endif %}
        {% endfor %}
    </div>

    <div class="api-note">
        API endpoint: <span class="endpoint">GET /api/profile?username=&lt;name&gt;</span><br>
        Used internally to load profile data dynamically.
    </div>

    <div id="api-result"></div>
</div>

<script>
function loadProfile() {
    const username = document.getElementById('username-input').value;
    fetch('/api/profile?username=' + encodeURIComponent(username))
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
    return render_template_string(HTML, profiles=PROFILES, current_user=CURRENT_USER)

@app.route("/api/profile")
def api_profile():
    username = request.args.get("username", "")
    profile = PROFILES.get(username)
    if not profile:
        return jsonify({"error": "User not found"}), 404
    # No access control — returns full profile including private fields
    return jsonify(profile)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
