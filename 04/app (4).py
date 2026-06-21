from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

FLAG = "FLAG{xss_level_4_stored_xss_python}"

# In-memory "database"
comments = []

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevLog — Community Notes</title>
    <link href="https://fonts.googleapis.com/css2?family=Bitter:wght@400;600;700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg: #f6f3ef;
            --surface: #ffffff;
            --border: #ddd8d0;
            --ink: #1c1917;
            --muted: #78716c;
            --accent: #16a34a;
            --accent-light: #dcfce7;
            --tag: #e7e5e4;
        }

        body {
            background: var(--bg);
            color: var(--ink);
            font-family: 'Source Sans 3', sans-serif;
            min-height: 100vh;
            padding: 60px 20px;
        }

        .container {
            max-width: 640px;
            margin: 0 auto;
        }

        .site-label {
            font-size: 11px;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 10px;
        }

        h1 {
            font-family: 'Bitter', serif;
            font-size: 34px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
        }

        .sub {
            color: var(--muted);
            font-size: 15px;
            margin-bottom: 40px;
        }

        .post-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 28px;
            margin-bottom: 36px;
        }

        .post-box h2 {
            font-family: 'Bitter', serif;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--muted);
            letter-spacing: 0.01em;
        }

        .field { margin-bottom: 14px; }

        label {
            display: block;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 6px;
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 10px 14px;
            font-family: 'Source Sans 3', sans-serif;
            font-size: 15px;
            color: var(--ink);
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 4px;
            outline: none;
            transition: border-color 0.15s;
            resize: vertical;
        }

        input[type="text"]:focus, textarea:focus {
            border-color: var(--accent);
            background: #fff;
        }

        textarea { min-height: 90px; }

        button {
            padding: 10px 22px;
            background: var(--ink);
            color: #fff;
            border: none;
            border-radius: 4px;
            font-family: 'Source Sans 3', sans-serif;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.04em;
            cursor: pointer;
            transition: background 0.15s;
        }
        button:hover { background: var(--accent); }

        .feed-label {
            font-size: 11px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--muted);
            font-weight: 600;
            margin-bottom: 16px;
        }

        .comment-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 20px 24px;
            margin-bottom: 14px;
        }

        .comment-meta {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }

        .avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: var(--tag);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            color: var(--muted);
            flex-shrink: 0;
        }

        .comment-author {
            font-weight: 600;
            font-size: 14px;
        }

        .comment-time {
            font-size: 12px;
            color: var(--muted);
            margin-left: auto;
        }

        .comment-body {
            font-size: 15px;
            line-height: 1.65;
            color: var(--ink);
        }

        .empty {
            text-align: center;
            color: var(--muted);
            font-size: 14px;
            padding: 32px;
            border: 1px dashed var(--border);
            border-radius: 6px;
        }

        .hint-box {
            margin-top: 48px;
            padding-top: 20px;
            border-top: 1px dashed var(--border);
            font-size: 12px;
            color: var(--muted);
            line-height: 1.7;
        }
    </style>
</head>
<body>
<div class="container">

    <div class="site-label">DevLog · Community</div>
    <h1>Community Notes</h1>
    <p class="sub">Share thoughts. They stick around for everyone to see.</p>

    <div class="post-box">
        <h2>Leave a note</h2>
        <form method="POST" action="/post">
            <div class="field">
                <label>Username</label>
                <input type="text" name="username" placeholder="e.g. hacker42" maxlength="32" required>
            </div>
            <div class="field">
                <label>Message</label>
                <textarea name="message" placeholder="Write something..." required></textarea>
            </div>
            <button type="submit">Post Note</button>
        </form>
    </div>

    <div class="feed-label">{{ comments|length }} note{{ 's' if comments|length != 1 else '' }} posted</div>

    {% if comments %}
        {% for c in comments %}
        <div class="comment-card">
            <div class="comment-meta">
                <div class="avatar">{{ c.username[0].upper() }}</div>
                <span class="comment-author">{{ c.username }}</span>
                <span class="comment-time">just now</span>
            </div>
            <div class="comment-body">{{ c.message | safe }}</div>
        </div>
        {% endfor %}
    {% else %}
        <div class="empty">No notes yet — be the first.</div>
    {% endif %}

    <div class="hint-box">
        One field is rendered safely. The other one isn't.<br>
        Notes persist and show up for every visitor.
    </div>

</div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, comments=comments)

@app.route("/post", methods=["POST"])
def post():
    username = request.form.get("username", "").strip()
    message = request.form.get("message", "").strip()
    if username and message:
        comments.append({"username": username, "message": message})
    return redirect(url_for("index"))

@app.route("/flag")
def flag():
    return FLAG

if __name__ == "__main__":
    app.run(debug=True, port=5000)
