from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

FLAG = "FLAG{xss_level_9_href_javascript_bypass_python}"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkVault — Save & Share Links</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #0f172a; --surface: #1e293b; --border: #334155;
            --text: #e2e8f0; --muted: #64748b; --accent: #38bdf8; --accent-dim: rgba(56,189,248,0.1);
        }
        body { background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif; min-height: 100vh; padding: 60px 20px; }
        .container { max-width: 640px; margin: 0 auto; }
        .logo { font-size: 13px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 40px; }
        h1 { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 6px; }
        .sub { color: var(--muted); font-size: 15px; margin-bottom: 36px; }
        .card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 28px; margin-bottom: 20px; }
        .field { margin-bottom: 14px; }
        label { display: block; font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
        input[type="text"] { width: 100%; padding: 11px 14px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; font-family: 'DM Sans', sans-serif; font-size: 14px; color: var(--text); outline: none; transition: border-color 0.15s; }
        input[type="text"]:focus { border-color: var(--accent); }
        button { padding: 11px 22px; background: var(--accent); color: var(--bg); border: none; border-radius: 6px; font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 14px; cursor: pointer; transition: opacity 0.15s; }
        button:hover { opacity: 0.85; }
        .link-list { margin-top: 28px; }
        .link-item { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 18px; margin-bottom: 10px; display: flex; align-items: center; gap: 12px; }
        .link-icon { font-size: 20px; flex-shrink: 0; }
        .link-title { font-size: 14px; font-weight: 500; margin-bottom: 2px; }
        .link-url { font-size: 13px; color: var(--accent); }
        .link-url a { color: var(--accent); text-decoration: none; }
        .link-url a:hover { text-decoration: underline; }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">LinkVault</div>
    <h1>Save your links</h1>
    <p class="sub">Store and share URLs with your team.</p>

    <div class="card">
        <form method="POST" action="/add">
            <div class="field">
                <label>Title</label>
                <input type="text" name="title" placeholder="e.g. Anthropic Homepage" required>
            </div>
            <div class="field">
                <label>URL</label>
                <input type="text" name="url" placeholder="https://..." required>
            </div>
            <button type="submit">Save Link</button>
        </form>
    </div>

    {% if links %}
    <div class="link-list">
        {% for link in links %}
        <div class="link-item">
            <div class="link-icon">🔗</div>
            <div>
                <div class="link-title">{{ link.title }}</div>
                <div class="link-url"><a href="{{ link.url | safe }}">{{ link.url }}</a></div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</div>
</body>
</html>
"""

links = []

def sanitize_url(url):
    # Blocks http/https checks — but misses other schemes
    if re.search(r'<script', url, re.IGNORECASE):
        return "#"
    if re.search(r'on\w+=', url, re.IGNORECASE):
        return "#"
    return url

@app.route("/")
def index():
    return render_template_string(HTML, links=links)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    if title and url:
        clean_url = sanitize_url(url)
        links.append({"title": title, "url": clean_url})
    from flask import redirect, url_for
    return redirect(url_for("index"))

@app.route("/flag")
def flag():
    return FLAG

if __name__ == "__main__":
    app.run(debug=True, port=5000)
