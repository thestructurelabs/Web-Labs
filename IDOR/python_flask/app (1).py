from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Simulated database of orders
ORDERS = {
    1: {"id": 1, "user": "alice", "user_id": 101, "item": "Mechanical Keyboard", "total": "$129.99", "status": "Delivered", "address": "12 Maple St, Boston MA", "note": "Leave at door"},
    2: {"id": 2, "user": "bob",   "user_id": 102, "item": "USB-C Hub",           "total": "$49.99",  "status": "Shipped",   "address": "88 Oak Ave, Austin TX",  "note": "Ring the bell"},
    3: {"id": 3, "user": "carol", "user_id": 103, "item": "Monitor Stand",       "total": "$79.99",  "status": "Processing","address": "5 Pine Rd, Denver CO",   "note": ""},
    4: {"id": 4, "user": "admin", "user_id": 100, "item": "Laptop",              "total": "$1,899.99","status": "Delivered", "address": "1 HQ Blvd, San Francisco CA", "note": "FLAG{idor_level_1_order_id_enumeration}"},
}

# Currently logged-in user (simulated session)
CURRENT_USER_ID = 101
CURRENT_USER = "alice"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopTrack — My Orders</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #f9fafb; --white: #fff; --border: #e5e7eb;
            --ink: #111827; --muted: #6b7280; --accent: #2563eb;
            --accent-light: #eff6ff; --green: #059669; --green-light: #ecfdf5;
            --yellow: #d97706; --yellow-light: #fffbeb; --red: #dc2626; --red-light: #fef2f2;
        }
        body { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; min-height: 100vh; }
        nav {
            background: var(--white); border-bottom: 1px solid var(--border);
            padding: 0 40px; height: 58px; display: flex; align-items: center; justify-content: space-between;
            position: sticky; top: 0; z-index: 10;
        }
        .nav-logo { font-weight: 700; font-size: 18px; letter-spacing: -0.02em; }
        .nav-logo span { color: var(--accent); }
        .nav-user {
            display: flex; align-items: center; gap: 10px;
            font-size: 14px; font-weight: 500; color: var(--muted);
        }
        .nav-avatar {
            width: 32px; height: 32px; border-radius: 50%;
            background: var(--accent-light); color: var(--accent);
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 13px;
        }
        .container { max-width: 760px; margin: 0 auto; padding: 40px 24px; }
        .page-title { font-size: 24px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 6px; }
        .page-sub { color: var(--muted); font-size: 14px; margin-bottom: 32px; }

        /* Order list */
        .order-card {
            background: var(--white); border: 1px solid var(--border);
            border-radius: 10px; padding: 20px 24px; margin-bottom: 14px;
            display: flex; align-items: center; justify-content: space-between;
            transition: box-shadow 0.15s;
        }
        .order-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.07); }
        .order-left { display: flex; flex-direction: column; gap: 4px; }
        .order-id { font-size: 12px; font-weight: 600; color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; }
        .order-item { font-size: 15px; font-weight: 600; }
        .order-total { font-size: 14px; color: var(--muted); }
        .order-right { display: flex; align-items: center; gap: 14px; }
        .status-badge {
            font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 20px;
        }
        .status-delivered { background: var(--green-light); color: var(--green); }
        .status-shipped { background: var(--yellow-light); color: var(--yellow); }
        .status-processing { background: var(--accent-light); color: var(--accent); }
        .view-btn {
            padding: 8px 16px; background: var(--white); border: 1px solid var(--border);
            border-radius: 6px; font-family: 'Inter', sans-serif; font-size: 13px;
            font-weight: 600; color: var(--ink); cursor: pointer; text-decoration: none;
            transition: background 0.15s;
        }
        .view-btn:hover { background: var(--bg); }

        /* Order detail */
        .detail-card {
            background: var(--white); border: 1px solid var(--border);
            border-radius: 10px; overflow: hidden;
        }
        .detail-header {
            padding: 20px 24px; border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between;
        }
        .detail-header h2 { font-size: 18px; font-weight: 700; }
        .detail-body { padding: 24px; }
        .detail-row {
            display: flex; justify-content: space-between; align-items: flex-start;
            padding: 12px 0; border-bottom: 1px solid var(--border); font-size: 14px;
        }
        .detail-row:last-child { border-bottom: none; }
        .detail-label { color: var(--muted); font-weight: 500; }
        .detail-value { font-weight: 500; text-align: right; max-width: 60%; }
        .back-link {
            display: inline-flex; align-items: center; gap: 6px;
            font-size: 14px; font-weight: 500; color: var(--accent);
            text-decoration: none; margin-bottom: 20px;
        }
        .back-link:hover { text-decoration: underline; }

        /* Error */
        .error-box {
            background: var(--red-light); border: 1px solid #fecaca;
            border-radius: 10px; padding: 24px; text-align: center;
        }
        .error-box h2 { font-size: 18px; font-weight: 700; color: var(--red); margin-bottom: 8px; }
        .error-box p { color: var(--muted); font-size: 14px; }
    </style>
</head>
<body>
<nav>
    <div class="nav-logo">Shop<span>Track</span></div>
    <div class="nav-user">
        <div class="nav-avatar">{{ current_user[0].upper() }}</div>
        <span>{{ current_user }}</span>
    </div>
</nav>

<div class="container">

{% if order %}
    <a href="/" class="back-link">← Back to my orders</a>
    <div class="detail-card">
        <div class="detail-header">
            <h2>Order #{{ order.id }}</h2>
            <span class="status-badge status-{{ order.status.lower() }}">{{ order.status }}</span>
        </div>
        <div class="detail-body">
            <div class="detail-row">
                <span class="detail-label">Item</span>
                <span class="detail-value">{{ order.item }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Total</span>
                <span class="detail-value">{{ order.total }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Shipping Address</span>
                <span class="detail-value">{{ order.address }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Delivery Note</span>
                <span class="detail-value">{{ order.note if order.note else '—' }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Customer</span>
                <span class="detail-value">{{ order.user }}</span>
            </div>
        </div>
    </div>

{% elif error %}
    <div class="error-box">
        <h2>Access Denied</h2>
        <p>{{ error }}</p>
    </div>

{% else %}
    <div class="page-title">My Orders</div>
    <p class="page-sub">Logged in as <strong>{{ current_user }}</strong></p>

    {% for order in my_orders %}
    <div class="order-card">
        <div class="order-left">
            <div class="order-id">Order #{{ order.id }}</div>
            <div class="order-item">{{ order.item }}</div>
            <div class="order-total">{{ order.total }}</div>
        </div>
        <div class="order-right">
            <span class="status-badge status-{{ order.status.lower() }}">{{ order.status }}</span>
            <a href="/order/{{ order.id }}" class="view-btn">View Details</a>
        </div>
    </div>
    {% endfor %}
{% endif %}

</div>
</body>
</html>
"""

@app.route("/")
def index():
    my_orders = [o for o in ORDERS.values() if o["user_id"] == CURRENT_USER_ID]
    return render_template_string(HTML,
        current_user=CURRENT_USER,
        my_orders=my_orders,
        order=None,
        error=None
    )

@app.route("/order/<int:order_id>")
def order_detail(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return render_template_string(HTML,
            current_user=CURRENT_USER,
            my_orders=[],
            order=None,
            error="Order not found."
        )
    # ⚠️ Missing authorization check — any order_id works
    return render_template_string(HTML,
        current_user=CURRENT_USER,
        my_orders=[],
        order=order,
        error=None
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
