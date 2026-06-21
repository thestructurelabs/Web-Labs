from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopX — Product Search</title>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg: #0a0a0f;
            --surface: #13131a;
            --border: #1e1e2e;
            --accent: #7c3aed;
            --accent-glow: rgba(124, 58, 237, 0.3);
            --text: #e2e2f0;
            --muted: #6b6b80;
        }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'DM Sans', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 60px 20px;
        }

        /* background grid */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(124,58,237,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(124,58,237,0.04) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: 0;
        }

        .container {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 620px;
        }

        /* header */
        .logo {
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            font-size: 13px;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 48px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .logo::before {
            content: '';
            width: 8px; height: 8px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 12px var(--accent);
        }

        h1 {
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            font-size: 42px;
            line-height: 1.1;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }

        h1 span {
            color: var(--accent);
        }

        .subtitle {
            color: var(--muted);
            font-size: 15px;
            margin-bottom: 40px;
            font-weight: 300;
        }

        /* search box */
        .search-wrap {
            display: flex;
            gap: 0;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .search-wrap:focus-within {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        input[type="text"] {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            padding: 16px 20px;
            font-family: 'DM Sans', sans-serif;
            font-size: 15px;
            color: var(--text);
        }
        input::placeholder { color: var(--muted); }

        button {
            background: var(--accent);
            border: none;
            padding: 16px 28px;
            color: white;
            font-family: 'Syne', sans-serif;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: background 0.2s, box-shadow 0.2s;
        }
        button:hover {
            background: #6d28d9;
            box-shadow: 0 0 20px var(--accent-glow);
        }

        /* result */
        .result {
            margin-top: 28px;
            padding: 20px 24px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            font-size: 14px;
            color: var(--muted);
            line-height: 1.6;
        }
        .result strong {
            color: var(--text);
            font-weight: 500;
        }

        /* hint */
        .hint {
            margin-top: 48px;
            padding: 16px 20px;
            border: 1px dashed #1e1e2e;
            border-radius: 10px;
            font-size: 13px;
            color: #3d3d52;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .hint::before { content: '⚑'; font-size: 16px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">ShopX Platform</div>

        <h1>Search <span>Products</span></h1>
        <p class="subtitle">Find anything in our catalog instantly.</p>

        <form method="GET" action="/search">
            <div class="search-wrap">
                <input type="text" name="q" placeholder="e.g. laptop, headphones..." autocomplete="off">
                <button type="submit">SEARCH</button>
            </div>
        </form>

        {% if query %}
        <div class="result">
            Showing results for: <strong>{{ query | safe }}</strong>
        </div>
        {% endif %}

        <div class="hint">Something feels off about how this page handles your input...</div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, query="")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return render_template_string(HTML, query=query)

@app.route("/flag")
def flag():
    return "<h2 style='font-family:monospace;color:green'>FLAG{xss_level_1_reflected_python}</h2>"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
