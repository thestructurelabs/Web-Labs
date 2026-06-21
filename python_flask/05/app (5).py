from flask import Flask, request, render_template_string

app = Flask(__name__)

FLAG = "FLAG{xss_level_5_filter_bypass_python}"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopNest — Discover Products</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg: #f9f9fb;
            --white: #ffffff;
            --border: #e4e4e7;
            --ink: #18181b;
            --muted: #71717a;
            --accent: #2563eb;
            --accent-light: #eff6ff;
            --tag-bg: #f4f4f5;
        }

        body {
            background: var(--bg);
            color: var(--ink);
            font-family: 'Plus Jakarta Sans', sans-serif;
            min-height: 100vh;
        }

        /* NAV */
        nav {
            background: var(--white);
            border-bottom: 1px solid var(--border);
            padding: 0 40px;
            height: 58px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .nav-logo {
            font-weight: 700;
            font-size: 18px;
            letter-spacing: -0.02em;
            color: var(--ink);
        }

        .nav-logo span { color: var(--accent); }

        .nav-links {
            display: flex;
            gap: 28px;
            font-size: 14px;
            color: var(--muted);
            font-weight: 500;
        }

        /* HERO SEARCH */
        .hero {
            background: var(--white);
            border-bottom: 1px solid var(--border);
            padding: 52px 40px;
            text-align: center;
        }

        .hero h1 {
            font-size: 36px;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin-bottom: 8px;
        }

        .hero p {
            color: var(--muted);
            font-size: 15px;
            margin-bottom: 28px;
        }

        .search-bar {
            display: inline-flex;
            width: 100%;
            max-width: 520px;
            background: var(--bg);
            border: 1.5px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            transition: border-color 0.15s, box-shadow 0.15s;
        }

        .search-bar:focus-within {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
            background: var(--white);
        }

        .search-bar input {
            flex: 1;
            border: none;
            outline: none;
            background: transparent;
            padding: 13px 18px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 15px;
            color: var(--ink);
        }

        .search-bar input::placeholder { color: var(--muted); }

        .search-bar button {
            background: var(--accent);
            border: none;
            padding: 13px 24px;
            color: white;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.15s;
        }

        .search-bar button:hover { background: #1d4ed8; }

        /* RESULTS AREA */
        .results-area {
            max-width: 900px;
            margin: 40px auto;
            padding: 0 24px;
        }

        .results-meta {
            font-size: 14px;
            color: var(--muted);
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }

        .results-meta strong {
            color: var(--ink);
        }

        /* PRODUCT GRID */
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }

        .product-card {
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
            transition: box-shadow 0.15s, transform 0.15s;
        }

        .product-card:hover {
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }

        .product-img {
            width: 100%;
            height: 140px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 42px;
            background: var(--tag-bg);
        }

        .product-info { padding: 14px 16px; }

        .product-name {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .product-price {
            font-size: 15px;
            font-weight: 700;
            color: var(--accent);
        }

        .product-tag {
            display: inline-block;
            margin-top: 8px;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            background: var(--accent-light);
            color: var(--accent);
            border-radius: 4px;
        }

        /* EMPTY STATE */
        .empty {
            text-align: center;
            padding: 60px 20px;
            color: var(--muted);
            font-size: 15px;
        }

        .empty .icon { font-size: 36px; margin-bottom: 12px; }
    </style>
</head>
<body>

    <nav>
        <div class="nav-logo">Shop<span>Nest</span></div>
        <div class="nav-links">
            <span>Electronics</span>
            <span>Fashion</span>
            <span>Home</span>
            <span>Deals</span>
        </div>
    </nav>

    <div class="hero">
        <h1>Find your next favorite thing</h1>
        <p>Search across millions of products</p>
        <form method="GET" action="/search">
            <div class="search-bar">
                <input type="text" name="q" placeholder="Search products..." value="{{ query }}" autocomplete="off">
                <button type="submit">Search</button>
            </div>
        </form>
    </div>

    {% if query %}
    <div class="results-area">
        <div class="results-meta">
            Showing results for <strong>{{ query | safe }}</strong>
        </div>

        <div class="grid">
            <div class="product-card">
                <div class="product-img">💻</div>
                <div class="product-info">
                    <div class="product-name">Pro Laptop 15"</div>
                    <div class="product-price">$1,299</div>
                    <span class="product-tag">In Stock</span>
                </div>
            </div>
            <div class="product-card">
                <div class="product-img">🎧</div>
                <div class="product-info">
                    <div class="product-name">Wireless Headphones</div>
                    <div class="product-price">$249</div>
                    <span class="product-tag">Best Seller</span>
                </div>
            </div>
            <div class="product-card">
                <div class="product-img">📱</div>
                <div class="product-info">
                    <div class="product-name">Smartphone X12</div>
                    <div class="product-price">$899</div>
                    <span class="product-tag">New</span>
                </div>
            </div>
        </div>
    </div>
    {% endif %}

</body>
</html>
"""

def sanitize(user_input):
    if "script" in user_input.lower():
        return "[removed]"
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
