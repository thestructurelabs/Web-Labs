from flask import Flask, request, render_template_string

app = Flask(__name__)

FLAG = "FLAG{xss_level_6_case_insensitive_bypass_python}"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TravelFind — Search Destinations</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #f0f9ff; --white: #ffffff; --border: #e0f2fe;
            --ink: #0c1a2e; --muted: #64748b; --accent: #0284c7; --accent-light: #e0f2fe;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Plus Jakarta Sans', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 1px solid var(--border); padding: 0 40px; height: 58px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 18px; letter-spacing: -0.02em; }
        .nav-logo span { color: var(--accent); }
        .nav-links { display: flex; gap: 28px; font-size: 14px; color: var(--muted); font-weight: 500; }
        .hero { background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 64px 40px; text-align: center; color: white; }
        .hero h1 { font-size: 38px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 8px; }
        .hero p { font-size: 15px; opacity: 0.8; margin-bottom: 28px; }
        .search-bar { display: inline-flex; width: 100%; max-width: 540px; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.2); }
        .search-bar input { flex: 1; border: none; outline: none; background: transparent; padding: 15px 20px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; color: var(--ink); }
        .search-bar input::placeholder { color: var(--muted); }
        .search-bar button { background: var(--accent); border: none; padding: 15px 28px; color: white; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 600; font-size: 14px; cursor: pointer; }
        .search-bar button:hover { background: #0369a1; }
        .results-area { max-width: 860px; margin: 40px auto; padding: 0 24px; }
        .results-meta { font-size: 14px; color: var(--muted); margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }
        .results-meta strong { color: var(--ink); }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
        .card { background: var(--white); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; transition: box-shadow 0.15s, transform 0.15s; }
        .card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); transform: translateY(-2px); }
        .card-img { width: 100%; height: 130px; display: flex; align-items: center; justify-content: center; font-size: 48px; background: var(--accent-light); }
        .card-info { padding: 14px 16px; }
        .card-name { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
        .card-price { font-size: 15px; font-weight: 700; color: var(--accent); }
        .card-tag { display: inline-block; margin-top: 8px; font-size: 11px; font-weight: 600; padding: 3px 8px; background: var(--accent-light); color: var(--accent); border-radius: 4px; }
    </style>
</head>
<body>
    <nav>
        <div class="nav-logo">Travel<span>Find</span></div>
        <div class="nav-links"><span>Flights</span><span>Hotels</span><span>Tours</span><span>Deals</span></div>
    </nav>
    <div class="hero">
        <h1>Where do you want to go?</h1>
        <p>Search thousands of destinations worldwide</p>
        <form method="GET" action="/search">
            <div class="search-bar">
                <input type="text" name="q" placeholder="City, country or landmark..." value="{{ query }}" autocomplete="off">
                <button type="submit">Search</button>
            </div>
        </form>
    </div>
    {% if query %}
    <div class="results-area">
        <div class="results-meta">Showing results for <strong>{{ query | safe }}</strong></div>
        <div class="grid">
            <div class="card"><div class="card-img">🗼</div><div class="card-info"><div class="card-name">Paris, France</div><div class="card-price">from $699</div><span class="card-tag">Popular</span></div></div>
            <div class="card"><div class="card-img">🏯</div><div class="card-info"><div class="card-name">Tokyo, Japan</div><div class="card-price">from $899</div><span class="card-tag">Trending</span></div></div>
            <div class="card"><div class="card-img">🏖️</div><div class="card-info"><div class="card-name">Bali, Indonesia</div><div class="card-price">from $549</div><span class="card-tag">Hot Deal</span></div></div>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""

def sanitize(user_input):
    # Only strips exact lowercase "script" — nothing else
    return user_input.replace("script", "")

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
