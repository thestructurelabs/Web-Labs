from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

FLAG = "FLAG{xss_level_8_event_handler_bypass_python}"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsDaily — Latest Headlines</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #f8f6f1; --white: #ffffff; --border: #e8e0d0;
            --ink: #1a1208; --muted: #8b7d6b; --accent: #c0392b; --accent-light: #fdf2f0;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Source Sans 3', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 3px solid var(--ink); padding: 0 40px; height: 60px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; }
        .nav-logo span { color: var(--accent); }
        .nav-links { display: flex; gap: 24px; font-size: 13px; color: var(--muted); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
        .hero { background: var(--white); border-bottom: 1px solid var(--border); padding: 48px 40px; text-align: center; }
        .hero h1 { font-family: 'Playfair Display', serif; font-size: 34px; margin-bottom: 8px; }
        .hero p { color: var(--muted); font-size: 15px; margin-bottom: 24px; }
        .search-bar { display: inline-flex; width: 100%; max-width: 540px; background: var(--bg); border: 1.5px solid var(--border); border-radius: 4px; overflow: hidden; }
        .search-bar:focus-within { border-color: var(--ink); }
        .search-bar input { flex: 1; border: none; outline: none; background: transparent; padding: 13px 18px; font-family: 'Source Sans 3', sans-serif; font-size: 15px; color: var(--ink); }
        .search-bar input::placeholder { color: var(--muted); }
        .search-bar button { background: var(--ink); border: none; padding: 13px 24px; color: white; font-family: 'Source Sans 3', sans-serif; font-weight: 600; font-size: 14px; cursor: pointer; }
        .search-bar button:hover { background: var(--accent); }
        .results-area { max-width: 760px; margin: 40px auto; padding: 0 24px; }
        .results-meta { font-size: 14px; color: var(--muted); margin-bottom: 20px; padding-bottom: 14px; border-bottom: 2px solid var(--ink); }
        .results-meta strong { color: var(--ink); font-family: 'Playfair Display', serif; }
        .article { background: var(--white); border: 1px solid var(--border); border-radius: 4px; padding: 20px 24px; margin-bottom: 12px; }
        .article-label { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
        .article-title { font-family: 'Playfair Display', serif; font-size: 18px; margin-bottom: 6px; }
        .article-meta { font-size: 13px; color: var(--muted); }
    </style>
</head>
<body>
    <nav>
        <div class="nav-logo">News<span>Daily</span></div>
        <div class="nav-links"><span>World</span><span>Tech</span><span>Business</span><span>Opinion</span></div>
    </nav>
    <div class="hero">
        <h1>Search the Archive</h1>
        <p>Millions of articles at your fingertips</p>
        <form method="GET" action="/search">
            <div class="search-bar">
                <input type="text" name="q" placeholder="Search headlines..." value="{{ query }}" autocomplete="off">
                <button type="submit">Search</button>
            </div>
        </form>
    </div>
    {% if query %}
    <div class="results-area">
        <div class="results-meta">Results for <strong>{{ query | safe }}</strong></div>
        <div class="article"><div class="article-label">Technology</div><div class="article-title">The Future of AI in Everyday Life</div><div class="article-meta">2 hours ago · 5 min read</div></div>
        <div class="article"><div class="article-label">Business</div><div class="article-title">Markets Reach All-Time High Amid Optimism</div><div class="article-meta">4 hours ago · 3 min read</div></div>
        <div class="article"><div class="article-label">World</div><div class="article-title">Global Leaders Meet at Climate Summit</div><div class="article-meta">6 hours ago · 7 min read</div></div>
    </div>
    {% endif %}
</body>
</html>
"""

def sanitize(user_input):
    # Blocks <script> tags and common event handlers
    user_input = re.sub(r'<script.*?>.*?</script>', '', user_input, flags=re.IGNORECASE | re.DOTALL)
    user_input = re.sub(r'on(click|load|mouseover|focus|blur)=', '', user_input, flags=re.IGNORECASE)
    return user_input

@app.route("/")
def index():
    return render_template_string(HTML, query="")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    clean = sanitize(query)
    return render_template_string(HTML, query=clean)

@app.route("/flag")
def flag():
    return FLAG

if __name__ == "__main__":
    app.run(debug=True, port=5000)
