from flask import Flask,render_template,request,redirect,url_for , session
from database import db
import re
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

@app.route('/') 
@app.route('/login', methods=['GET','POST'])
def login(): 
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=db.cur
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = %s',(username,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['username']=account['username']
            msg="Logged in successfully !"
            return render_template('index.html',msg=msg)
        else:
            msg="Incorrect username /password !"

    return render_template('login.html', msg=msg) 
  



@app.route('/register', methods=['POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        cursor = db.cur
        cursor.execute('SELECT id FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not (username and password and email):
            msg = 'Please fill out the form!'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, hashed_password, email))
            db.conn.commit()
            return redirect(url_for('login'))  # Redirect to login page after successful registration

    return render_template('register.html', msg=msg)