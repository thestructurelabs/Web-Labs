from flask import Flask, request, render_template_string, redirect, url_for
import re

app = Flask(__name__)

FLAG = "FLAG{xss_level_10_csp_bypass_python}"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FeedbackHub — Share Your Thoughts</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #f9fafb; --white: #ffffff; --border: #e5e7eb;
            --ink: #111827; --muted: #6b7280; --accent: #059669; --accent-light: #ecfdf5;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; padding: 60px 20px; }
        .container { max-width: 620px; margin: 0 auto; }
        .logo { font-size: 12px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); margin-bottom: 36px; }
        h1 { font-size: 30px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 6px; }
        .sub { color: var(--muted); font-size: 15px; margin-bottom: 36px; }
        .card { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 28px; margin-bottom: 28px; }
        .field { margin-bottom: 16px; }
        label { display: block; font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
        input[type="text"], textarea { width: 100%; padding: 11px 14px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; font-family: 'Inter', sans-serif; font-size: 14px; color: var(--ink); outline: none; transition: border-color 0.15s; resize: vertical; }
        input[type="text"]:focus, textarea:focus { border-color: var(--accent); }
        textarea { min-height: 100px; }
        button { padding: 11px 24px; background: var(--ink); color: white; border: none; border-radius: 6px; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 14px; cursor: pointer; }
        button:hover { background: var(--accent); }
        .feedback-item { background: var(--white); border: 1px solid var(--border); border-radius: 8px; padding: 16px 20px; margin-bottom: 10px; }
        .fb-name { font-weight: 600; font-size: 14px; margin-bottom: 4px; }
        .fb-msg { font-size: 14px; color: var(--muted); line-height: 1.6; }
        .fb-template { font-size: 13px; margin-top: 8px; color: var(--ink); border-top: 1px solid var(--border); padding-top: 8px; }
        .count { font-size: 13px; color: var(--muted); margin-bottom: 16px; }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">FeedbackHub</div>
    <h1>Leave your feedback</h1>
    <p class="sub">Tell us what you think. We read everything.</p>

    <div class="card">
        <form method="POST" action="/submit">
            <div class="field">
                <label>Name</label>
                <input type="text" name="name" placeholder="Your name" required>
            </div>
            <div class="field">
                <label>Message</label>
                <textarea name="message" placeholder="Your feedback..." required></textarea>
            </div>
            <div class="field">
                <label>Template Style</label>
                <input type="text" name="template" placeholder='e.g. "bold" or "italic"'>
            </div>
            <button type="submit">Submit Feedback</button>
        </form>
    </div>

    {% if feedbacks %}
    <div class="count">{{ feedbacks|length }} response(s)</div>
    {% for fb in feedbacks %}
    <div class="feedback-item">
        <div class="fb-name">{{ fb.name }}</div>
        <div class="fb-msg">{{ fb.message }}</div>
        <div class="fb-template">Style: {{ fb.template | safe }}</div>
    </div>
    {% endfor %}
    {% endif %}
</div>
</body>
</html>
"""

feedbacks = []

def sanitize(text):
    # Strips tags and common event handlers — fairly aggressive
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<[^>]+on\w+\s*=\s*["\'][^"\']*["\'][^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    # Allows "safe" HTML tags for styling
    text = re.sub(r'<(?!\/?(b|i|u|em|strong|span|br)\b)[^>]+>', '', text, flags=re.IGNORECASE)
    return text

@app.route("/")
def index():
    return render_template_string(HTML, feedbacks=feedbacks)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()
    template = request.form.get("template", "").strip()
    if name and message:
        feedbacks.append({
            "name": name,
            "message": sanitize(message),
            "template": template  # template field is NOT sanitized
        })
    return redirect(url_for("index"))

@app.route("/flag")
def flag():
    return FLAG

if __name__ == "__main__":
    app.run(debug=True, port=5000)
