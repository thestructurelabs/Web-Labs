from flask import Flask, request, render_template_string

app = Flask(__name__)

FLAG = "FLAG{xss_level_3_dom_based_hash_injection}"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SearchHub — Find Anything</title>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg: #0d0f12;
            --surface: #161a20;
            --border: #252b35;
            --text: #e2e8f0;
            --muted: #64748b;
            --accent: #38bdf8;
            --accent-dim: #0c4a6e;
            --danger: #f87171;
            --mono: 'IBM Plex Mono', monospace;
            --sans: 'IBM Plex Sans', sans-serif;
        }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: var(--sans);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 80px 20px 60px;
        }

        .logo {
            font-family: var(--mono);
            font-size: 13px;
            letter-spacing: 0.15em;
            color: var(--accent);
            text-transform: uppercase;
            margin-bottom: 48px;
            opacity: 0.8;
        }

        .logo span {
            color: var(--muted);
        }

        h1 {
            font-size: 42px;
            font-weight: 600;
            letter-spacing: -0.03em;
            margin-bottom: 12px;
            text-align: center;
        }

        h1 em {
            font-style: normal;
            color: var(--accent);
        }

        .tagline {
            color: var(--muted);
            font-size: 15px;
            margin-bottom: 48px;
            text-align: center;
        }

        .search-wrap {
            width: 100%;
            max-width: 560px;
            position: relative;
            margin-bottom: 40px;
        }

        .search-wrap input {
            width: 100%;
            padding: 16px 56px 16px 20px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            font-family: var(--mono);
            font-size: 15px;
            color: var(--text);
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .search-wrap input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-dim);
        }

        .search-wrap button {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            background: var(--accent);
            border: none;
            border-radius: 4px;
            padding: 6px 14px;
            font-family: var(--sans);
            font-size: 13px;
            font-weight: 600;
            color: var(--bg);
            cursor: pointer;
            transition: opacity 0.15s;
        }

        .search-wrap button:hover { opacity: 0.85; }

        .results-box {
            width: 100%;
            max-width: 560px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 20px 24px;
            min-height: 80px;
            display: none;
        }

        .results-label {
            font-family: var(--mono);
            font-size: 11px;
            letter-spacing: 0.12em;
            color: var(--muted);
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        #result-output {
            font-size: 15px;
            color: var(--text);
            line-height: 1.6;
        }

        .hint-box {
            margin-top: 48px;
            max-width: 560px;
            border-top: 1px dashed var(--border);
            padding-top: 24px;
            font-family: var(--mono);
            font-size: 12px;
            color: var(--muted);
            line-height: 1.8;
            text-align: center;
        }

        .hint-box strong {
            color: var(--accent);
        }

        .footer {
            margin-top: 60px;
            font-family: var(--mono);
            font-size: 11px;
            color: var(--border);
            letter-spacing: 0.1em;
        }
    </style>
</head>
<body>

    <div class="logo">Search<span>/</span>Hub</div>

    <h1>Find <em>anything</em>.</h1>
    <p class="tagline">Results update instantly — no page reload needed.</p>

    <div class="search-wrap">
        <input type="text" id="search-input" placeholder="Type your query..." autocomplete="off">
        <button onclick="doSearch()">Go</button>
    </div>

    <div class="results-box" id="results-box">
        <div class="results-label">Results for</div>
        <div id="result-output"></div>
    </div>

    <div class="hint-box">
        <strong>Hint:</strong> This page never talks to the server after load.<br>
        Your query lives somewhere the server never sees.<br>
        The display reads directly from there — no sanitization.
    </div>

    <div class="footer">// dom-based · client-side · no server roundtrip</div>

    <script>
        function getQuery() {
            // Reads the search term from the URL fragment
            return decodeURIComponent(window.location.hash.slice(1));
        }

        function doSearch() {
            const q = document.getElementById('search-input').value;
            window.location.hash = encodeURIComponent(q);
            renderResults();
        }

        function renderResults() {
            const query = getQuery();
            if (!query) return;

            const box = document.getElementById('results-box');
            const output = document.getElementById('result-output');

            box.style.display = 'block';
            // Vulnerable: directly writes unsanitized hash content into innerHTML
            output.innerHTML = 'Showing results for: <strong>' + query + '</strong>';
        }

        // Auto-render if hash is already set on page load
        window.addEventListener('load', renderResults);
        window.addEventListener('hashchange', renderResults);
    </script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/flag")
def flag():
    return FLAG

if __name__ == "__main__":
    app.run(debug=True, port=5000)
