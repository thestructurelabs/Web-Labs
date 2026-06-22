from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

USERS = {
    101: {"name": "alice", "email": "alice@example.com", "plan": "Free"},
    102: {"name": "bob",   "email": "bob@example.com",   "plan": "Pro"},
    103: {"name": "carol", "email": "carol@example.com", "plan": "Pro"},
    100: {"name": "admin", "email": "admin@shoptrack.io", "plan": "Enterprise", "secret": "FLAG{idor_level_2_hidden_input_user_id}"},
}

CURRENT_USER_ID = 101

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AccountHub — Settings</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #f9fafb; --white: #fff; --border: #e5e7eb;
            --ink: #111827; --muted: #6b7280; --accent: #7c3aed; --accent-light: #f5f3ff;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 1px solid var(--border); padding: 0 40px; height: 58px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 18px; }
        .nav-logo span { color: var(--accent); }
        .nav-user { font-size: 14px; color: var(--muted); font-weight: 500; }
        .container { max-width: 680px; margin: 0 auto; padding: 44px 24px; }
        h1 { font-size: 24px; font-weight: 700; margin-bottom: 6px; }
        .sub { color: var(--muted); font-size: 14px; margin-bottom: 32px; }
        .card { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 28px; margin-bottom: 20px; }
        .card-title { font-size: 15px; font-weight: 600; margin-bottom: 20px; padding-bottom: 14px; border-bottom: 1px solid var(--border); }
        .field { margin-bottom: 18px; }
        label { display: block; font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
        input[type="text"], input[type="email"] {
            width: 100%; padding: 11px 14px; background: var(--bg); border: 1px solid var(--border);
            border-radius: 6px; font-family: 'Inter', sans-serif; font-size: 14px; color: var(--ink);
            outline: none; transition: border-color 0.15s;
        }
        input:focus { border-color: var(--accent); }
        .plan-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; background: var(--accent-light); color: var(--accent); }
        .save-btn { padding: 11px 24px; background: var(--accent); color: white; border: none; border-radius: 6px; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 14px; cursor: pointer; }
        .save-btn:hover { background: #6d28d9; }
        .profile-viewed { background: var(--accent-light); border: 1px solid #ddd6fe; border-radius: 10px; padding: 20px 24px; margin-top: 20px; }
        .profile-viewed h3 { font-size: 15px; font-weight: 600; margin-bottom: 14px; color: var(--accent); }
        .pv-row { display: flex; justify-content: space-between; font-size: 14px; padding: 8px 0; border-bottom: 1px solid #ede9fe; }
        .pv-row:last-child { border-bottom: none; }
        .pv-label { color: var(--muted); }
        .pv-value { font-weight: 500; }
    </style>
</head>
<body>
<nav>
    <div class="nav-logo">Account<span>Hub</span></div>
    <div class="nav-user">Logged in as <strong>{{ current_user.name }}</strong></div>
</nav>
<div class="container">
    <h1>Account Settings</h1>
    <p class="sub">Manage your profile and preferences.</p>

    <div class="card">
        <div class="card-title">Personal Information</div>
        <form method="POST" action="/save-profile">
            <!-- user_id identifies which profile to update -->
            <input type="hidden" name="user_id" value="{{ current_user_id }}">
            <div class="field">
                <label>Full Name</label>
                <input type="text" name="name" value="{{ current_user.name }}">
            </div>
            <div class="field">
                <label>Email Address</label>
                <input type="email" name="email" value="{{ current_user.email }}">
            </div>
            <div class="field">
                <label>Current Plan</label><br>
                <span class="plan-badge">{{ current_user.plan }}</span>
            </div>
            <button type="submit" class="save-btn">Save Changes</button>
        </form>
    </div>

    {% if viewed %}
    <div class="profile-viewed">
        <h3>Profile Data Loaded</h3>
        {% for k, v in viewed.items() %}
        <div class="pv-row">
            <span class="pv-label">{{ k }}</span>
            <span class="pv-value">{{ v }}</span>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def index():
    user = USERS[CURRENT_USER_ID]
    return render_template_string(HTML,
        current_user=user,
        current_user_id=CURRENT_USER_ID,
        viewed=None
    )

@app.route("/save-profile", methods=["POST"])
def save_profile():
    # Takes user_id from POST body — no verification against session
    user_id = int(request.form.get("user_id", CURRENT_USER_ID))
    user = USERS.get(user_id, USERS[CURRENT_USER_ID])
    return render_template_string(HTML,
        current_user=USERS[CURRENT_USER_ID],
        current_user_id=CURRENT_USER_ID,
        viewed=user
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
