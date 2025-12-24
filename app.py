from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "secret123"

# RDS config
app.config['MYSQL_HOST'] = 'RDS-ENDPOINT'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'userdb'

mysql = MySQL(app)

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/home')
def home():
    if 'user' in session:
        return render_template("home.html", user=session['user'])
    return redirect('/')

@app.route('/register_user', methods=['POST'])
def register_user():
    user = request.form['username']
    pwd = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)", (user, pwd))
    mysql.connection.commit()
    return redirect('/')

@app.route('/login_user', methods=['POST'])
def login_user():
    user = request.form['username']
    pwd = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
    result = cur.fetchone()
    if result:
        session['user'] = user
        return redirect('/home')
    return "Invalid Login"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
