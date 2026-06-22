from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# Simulated file storage
FILES = {
    1: {"id": 1, "owner_id": 101, "name": "Q1_Report_Draft.pdf",      "size": "2.1 MB", "type": "PDF",  "content": "Quarterly sales figures for internal review."},
    2: {"id": 2, "owner_id": 101, "name": "Team_Meeting_Notes.docx",  "size": "0.4 MB", "type": "DOCX", "content": "Notes from the weekly sync on March 12."},
    3: {"id": 3, "owner_id": 102, "name": "Budget_2024_Final.xlsx",   "size": "1.8 MB", "type": "XLSX", "content": "Annual budget approved by finance."},
    4: {"id": 4, "owner_id": 103, "name": "Design_Assets_v3.zip",     "size": "48 MB",  "type": "ZIP",  "content": "Brand guidelines and logo exports."},
    5: {"id": 5, "owner_id": 100, "name": "admin_credentials.txt",    "size": "0.1 MB", "type": "TXT",  "content": "FLAG{idor_level_4_file_download_id}"},
}

CURRENT_USER_ID = 101
MY_FILES = [f for f in FILES.values() if f["owner_id"] == CURRENT_USER_ID]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocVault — My Files</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #f8fafc; --white: #fff; --border: #e2e8f0;
            --ink: #0f172a; --muted: #64748b; --accent: #0ea5e9; --accent-light: #f0f9ff;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav { background: var(--white); border-bottom: 1px solid var(--border); padding: 0 40px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-weight: 700; font-size: 17px; }
        .nav-logo span { color: var(--accent); }
        .nav-user { font-size: 13px; color: var(--muted); }
        .container { max-width: 800px; margin: 0 auto; padding: 40px 24px; }
        .page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 28px; }
        h1 { font-size: 22px; font-weight: 700; }
        .file-count { font-size: 13px; color: var(--muted); }
        table { width: 100%; border-collapse: collapse; background: var(--white); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
        th { text-align: left; padding: 12px 18px; font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); border-bottom: 1px solid var(--border); background: var(--bg); }
        td { padding: 14px 18px; font-size: 14px; border-bottom: 1px solid var(--border); }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: var(--accent-light); }
        .file-icon { font-size: 18px; margin-right: 8px; }
        .file-name { font-weight: 500; }
        .file-type { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; background: var(--accent-light); color: var(--accent); }
        .dl-btn { padding: 6px 14px; background: var(--white); border: 1px solid var(--border); border-radius: 6px; font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: var(--ink); cursor: pointer; text-decoration: none; transition: background 0.15s; }
        .dl-btn:hover { background: var(--bg); }
        #preview { margin-top: 24px; background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 20px 24px; display: none; }
        #preview h3 { font-size: 15px; font-weight: 600; margin-bottom: 12px; }
        #preview-content { font-size: 14px; color: var(--muted); font-family: monospace; }
    </style>
</head>
<body>
<nav>
    <div class="nav-logo">Doc<span>Vault</span></div>
    <div class="nav-user">Logged in as user #{{ current_user_id }}</div>
</nav>
<div class="container">
    <div class="page-header">
        <h1>My Files</h1>
        <span class="file-count">{{ files|length }} files</span>
    </div>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Size</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for f in files %}
            <tr>
                <td><span class="file-icon">📄</span><span class="file-name">{{ f.name }}</span></td>
                <td><span class="file-type">{{ f.type }}</span></td>
                <td>{{ f.size }}</td>
                <td><a class="dl-btn" onclick="previewFile({{ f.id }})">Download</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div id="preview">
        <h3 id="preview-title">File Preview</h3>
        <div id="preview-content"></div>
    </div>
</div>
<script>
function previewFile(fileId) {
    fetch('/api/file?id=' + fileId)
        .then(r => r.json())
        .then(data => {
            document.getElementById('preview').style.display = 'block';
            document.getElementById('preview-title').textContent = data.name || 'File Preview';
            document.getElementById('preview-content').textContent = data.content || data.error;
        });
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    my_files = [f for f in FILES.values() if f["owner_id"] == CURRENT_USER_ID]
    return render_template_string(HTML, files=my_files, current_user_id=CURRENT_USER_ID)

@app.route("/api/file")
def api_file():
    file_id = request.args.get("id", type=int)
    f = FILES.get(file_id)
    if not f:
        return jsonify({"error": "File not found"}), 404
    # Missing ownership check
    return jsonify(f)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
