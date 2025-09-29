from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
import mysql.connector, os, time

app = Flask(__name__)
auth = HTTPBasicAuth()

# ====== Credentials for Basic Auth (set via ENV) ======
APP_USER = os.getenv("APP_USER", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "secret")

@auth.verify_password
def verify_password(username, password):
    return username == APP_USER and password == APP_PASSWORD

# (Optional) custom unauthorized message
@auth.error_handler
def unauthorized():
    return Response("Unauthorized", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

# ====== MySQL config ======
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "db"),
    "user": os.getenv("MYSQL_USER", "appuser"),
    "password": os.getenv("MYSQL_PASSWORD", "AppPass123!"),
    "database": os.getenv("MYSQL_DB", "mydb"),
}

def get_conn(retries=30, delay=2):
    last_err = None
    for _ in range(retries):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Exception as e:
            last_err = e
            time.sleep(delay)
    raise last_err

# ====== Routes ======
@app.route("/health")
def health():
    # Route không cần auth (tiện cho healthcheck)
    return "OK"

@app.route("/")
@auth.login_required
def index():
    return (
        "<h2>Flask + MySQL + phpMyAdmin</h2>"
        "<ul>"
        "<li><a href='/init'>/init</a> – create table</li>"
        "<li><a href='/add?msg=Hello'>/add?msg=Hello</a> – insert a row</li>"
        "<li><a href='/list'>/list</a> – list rows</li>"
        "</ul>"
        "<p>phpMyAdmin: open <code>:8080</code>, login with the user in <code>.env</code></p>"
    )

@app.route("/init")
@auth.login_required
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    return "OK: created table messages"

@app.route("/add")
@auth.login_required
def add():
    msg = request.args.get("msg", "Hello from Flask")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content) VALUES (%s)", (msg,))
    conn.commit()
    cur.close()
    conn.close()
    return f"Inserted: {msg}"

@app.route("/list")
@auth.login_required
def list_msgs():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    html = ["<h3>Latest messages</h3><ul>"]
    for rid, content, ts in rows:
        html.append(f"<li>#{rid} | {content} | {ts}</li>")
    html.append("</ul>")
    return "\n".join(html)

if __name__ == "__main__":
    # Chạy app (Basic Auth áp dụng cho các route đã đánh dấu)
    app.run(host="0.0.0.0", port=5000)
