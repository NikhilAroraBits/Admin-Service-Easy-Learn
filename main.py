from flask import Flask, render_template, redirect, url_for, session,request
from flask_mysqldb import MySQL
import MySQLdb
import random

app = Flask(__name__)
app.secret_key = "123456"

app.config["MYSQL_HOST"] = "scalableservicesassignment.cz1kzfagdqhy.ap-south-1.rds.amazonaws.com"
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "123Amazon"
app.config["MYSQL_DB"] = "AdminInfo"

db = MySQL(app)

@app.route ( '/index' )
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('Sign up') :
         return redirect(url_for('AdminSignup'))  

        if 'email' in request.form and 'password' in request.form and 'Log In' in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM AdminInfo.adminlogin WHERE email= %s AND Password = %s", (email,password))
            info = cursor.fetchone()

            if info is not None and info['Email'] == email and info['Password'] == password:
                session['loginsuccess'] = True
                return redirect(url_for('CourseAddition'))
            else:
                return "Login Error"

    return render_template("login.html")

@app.route('/CourseAddition', methods=['GET', 'POST'])
def CourseAddition():
    if request.method == 'POST':
        if 'course-name' in request.form and 'course-description' in request.form and 'link-video' in request.form:
            courseName = request.form['course-name']
            courseDescription = request.form['course-description']
            courseVideoLink = request.form['link-video']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            choices = list(range(100))
            random.shuffle(choices)
            id= 2000 + choices.pop()
            cursor.execute("INSERT INTO Course.CourseVideo (ID, Title, Description, Link) VALUES (%s, %s, %s, %s)", (id, courseName, courseDescription, courseVideoLink))
            db.connection.commit()
            return 'Registration Successful !!'

    elif session['loginsuccess']:
        return render_template("CourseAddition.html")

    else:
        return "Error"


@app.route('/AdminSignup', methods=['GET', 'POST'])
def AdminSignup():
    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form and 'name' in request.form:
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO AdminInfo.adminlogin (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            db.connection.commit()
            return redirect(url_for('index'))
           

    return render_template("SignUp.html")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
    app.run(debug=True)
