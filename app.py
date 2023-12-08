from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'




# Load database configuration from a YAML file or set your database config here

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'

mysql = MySQL(app)



@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM tbl_users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
    try:
        print("MySql Connection object:", mysql.connection )
        cur = mysql.connection.cursor()
    except AttributeError as e:
        print("Attribute Error:", e)

        if user and pwd == user[1]:
            session['username'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = None
        try:
            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO tbl_users (username, password) values ('{username}', '{pwd}')")
            mysql.connection.commit()
            return redirect(url_for('login'))
        except Exception as e:
            print("An error occured:" , e)
        finally:
            if cur:
                 cur.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))


if __name__ == '__main__':
   app.run(debug=True)