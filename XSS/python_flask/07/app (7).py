from flask import Flask, request, render_template_string

app = Flask(__name__)

FLAG = "FLAG{xss_level_7_recursive_filter_bypass_python}"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JobBoard — Find Your Role</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #fafafa; --white: #ffffff; --border: #e5e7eb;
            --ink: #111827; --muted: #6b7280; --accent: #7c3aed; --accent-light: #f5f3ff;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 1px solid var(--border); padding: 0 40px; height: 60px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 17px; }
        .nav-logo span { color: var(--accent); }
        .nav-links { display: flex; gap: 24px; font-size: 14px; color: var(--muted); font-weight: 500; }
        .hero { background: var(--white); border-bottom: 1px solid var(--border); padding: 56px 40px; text-align: center; }
        .hero h1 { font-size: 36px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 8px; }
        .hero p { color: var(--muted); font-size: 15px; margin-bottom: 28px; }
        .search-bar { display: inline-flex; width: 100%; max-width: 540px; background: var(--bg); border: 1.5px solid var(--border); border-radius: 8px; overflow: hidden; transition: border-color 0.15s, box-shadow 0.15s; }
        .search-bar:focus-within { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(124,58,237,0.1); }
        .search-bar input { flex: 1; border: none; outline: none; background: transparent; padding: 14px 18px; font-family: 'Inter', sans-serif; font-size: 15px; color: var(--ink); }
        .search-bar input::placeholder { color: var(--muted); }
        .search-bar button { background: var(--accent); border: none; padding: 14px 26px; color: white; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 14px; cursor: pointer; }
        .search-bar button:hover { background: #6d28d9; }
        .results-area { max-width: 760px; margin: 40px auto; padding: 0 24px; }
        .results-meta { font-size: 14px; color: var(--muted); margin-bottom: 20px; padding-bottom: 14px; border-bottom: 1px solid var(--border); }
        .results-meta strong { color: var(--ink); }
        .job-card { background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 20px 24px; margin-bottom: 12px; display: flex; align-items: center; gap: 16px; transition: box-shadow 0.15s; }
        .job-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.07); }
        .job-logo { width: 46px; height: 46px; border-radius: 8px; background: var(--accent-light); display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }
        .job-title { font-weight: 600; font-size: 15px; margin-bottom: 4px; }
        .job-meta { font-size: 13px; color: var(--muted); }
        .job-tag { margin-left: auto; font-size: 12px; font-weight: 600; padding: 4px 10px; background: var(--accent-light); color: var(--accent); border-radius: 20px; flex-shrink: 0; }
    </style>
</head>
<body>
    <nav>
        <div class="nav-logo">Job<span>Board</span></div>
        <div class="nav-links"><span>Remote</span><span>Full-time</span><span>Startups</span><span>Saved</span></div>
    </nav>
    <div class="hero">
        <h1>Find your next opportunity</h1>
        <p>Search thousands of jobs from top companies</p>
        <form method="GET" action="/search">
            <div class="search-bar">
                <input type="text" name="q" placeholder="Job title, skill or company..." value="{{ query }}" autocomplete="off">
                <button type="submit">Search Jobs</button>
            </div>
        </form>
    </div>
    {% if query %}
    <div class="results-area">
        <div class="results-meta">Jobs matching <strong>{{ query | safe }}</strong></div>
        <div class="job-card"><div class="job-logo">🏢</div><div><div class="job-title">Senior Frontend Engineer</div><div class="job-meta">Stripe · San Francisco · $160k–$200k</div></div><span class="job-tag">Remote</span></div>
        <div class="job-card"><div class="job-logo">🚀</div><div><div class="job-title">Product Designer</div><div class="job-meta">Figma · New York · $130k–$160k</div></div><span class="job-tag">Hybrid</span></div>
        <div class="job-card"><div class="job-logo">💡</div><div><div class="job-title">Backend Engineer</div><div class="job-meta">Linear · Remote · $140k–$180k</div></div><span class="job-tag">Full-time</span></div>
    </div>
    {% endif %}
</body>
</html>
"""

def sanitize(user_input):
    # Removes "script" repeatedly until none remain
    import re
    while re.search(r'script', user_input, re.IGNORECASE):
        user_input = re.sub(r'script', '', user_input, flags=re.IGNORECASE)
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
