from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("users.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Students table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        department TEXT
    )
    """)

    # Sample data
    cur.execute("INSERT OR IGNORE INTO students VALUES (1, 'Marga Duguma', 'Electrical Engineering')")
    cur.execute("INSERT OR IGNORE INTO students VALUES (2, 'Abel Tesfaye', 'Computer Science')")
    cur.execute("INSERT OR IGNORE INTO students VALUES (3, 'Sara Ahmed', 'Information Technology')")

    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect("/")
        except:
            return "User already exists"

    return render_template("register.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect("/")

# ---------------- SEARCH ----------------
@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect("/")

    student = None

    if request.method == "POST":
        student_id = request.form["student_id"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
        student = cur.fetchone()
        conn.close()

    return render_template("search.html", student=student)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
