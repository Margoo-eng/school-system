from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "12345"

def get_db():
    return sqlite3.connect("students.db")

@app.route('/', methods=['GET','POST'])
def login():
    msg = ""
    if request.method == 'POST':
        sid = request.form['id']
        pwd = request.form['password']

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE id=? AND password=?", (sid, pwd))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = user[0]
            return redirect('/profile')
        else:
            msg = "Invalid login"

    return render_template("login.html", msg=msg)


@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/')

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id=?", (session['user'],))
    user = c.fetchone()
    conn.close()

    return render_template("profile.html", user=user)


@app.route('/search', methods=['GET','POST'])
def search():
    result = None

    if request.method == 'POST':
        sid = request.form['id']

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE id=?", (sid,))
        result = c.fetchone()
        conn.close()

    return render_template("search.html", result=result)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
