from flask import Flask, request, render_template_string

app = Flask(__name__)

FLAG = "FLAG{xss_level_2_attribute_breakout_python}"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AccountSettings — Profile</title>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Karla:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --paper: #faf5ee;
            --ink: #2b2521;
            --rule: #e6dccb;
            --accent: #c1553a;
            --muted: #9a8e7e;
        }

        body {
            background: var(--paper);
            color: var(--ink);
            font-family: 'Karla', sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            padding: 70px 20px;
            background-image: radial-gradient(circle at 1px 1px, var(--rule) 1px, transparent 0);
            background-size: 28px 28px;
        }

        .card {
            width: 100%;
            max-width: 480px;
            background: #fffdfa;
            border: 1px solid var(--rule);
            border-radius: 4px;
            padding: 44px 40px;
            box-shadow: 0 1px 0 var(--rule), 0 16px 40px -24px rgba(43,37,33,0.25);
        }

        .eyebrow {
            font-size: 11px;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 14px;
        }

        h1 {
            font-family: 'Fraunces', serif;
            font-weight: 600;
            font-size: 30px;
            line-height: 1.25;
            margin-bottom: 6px;
            letter-spacing: -0.01em;
        }

        .sub {
            color: var(--muted);
            font-size: 14px;
            margin-bottom: 32px;
        }

        hr {
            border: none;
            border-top: 1px solid var(--rule);
            margin: 28px 0;
        }

        label {
            display: block;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 8px;
        }

        input[type="text"] {
            width: 100%;
            padding: 12px 14px;
            font-family: 'Karla', sans-serif;
            font-size: 15px;
            color: var(--ink);
            border: 1px solid var(--rule);
            border-radius: 3px;
            background: var(--paper);
            outline: none;
            transition: border-color 0.15s, background 0.15s;
        }
        input[type="text"]:focus {
            border-color: var(--accent);
            background: #fff;
        }

        .field { margin-bottom: 20px; }

        button {
            margin-top: 8px;
            padding: 12px 22px;
            background: var(--ink);
            color: var(--paper);
            border: none;
            border-radius: 3px;
            font-family: 'Karla', sans-serif;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: background 0.15s;
        }
        button:hover { background: var(--accent); }

        .hint {
            margin-top: 36px;
            padding-top: 20px;
            border-top: 1px dashed var(--rule);
            font-size: 12px;
            color: var(--muted);
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="eyebrow">Account · Settings</div>
        <h1>Welcome back, {{ name }}</h1>
        <p class="sub">Manage how your name appears across the workspace.</p>

        <hr>

        <form method="GET" action="/">
            <div class="field">
                <label>Display Name</label>
                <input type="text" name="name" value="{{ name | safe }}">
            </div>
            <button type="submit">Save Changes</button>
        </form>

        <div class="hint">
            Two places on this page reflect your input. Only one of them forgets to escape it.
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    name = request.args.get("name", "Guest")
    return render_template_string(HTML, name=name)

@app.route("/flag")
def flag():
    return FLAG

if __name__ == "__main__":
    app.run(debug=True, port=5000)
