#!/usr/bin/env python

from sqlalchemy.orm import session
from flask import Flask, redirect, url_for, render_template, request, session
from models import db, login, User
from flask_login import current_user, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SEING'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
login.init_app(app)
login.login_view = 'login'


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    '''Homepage routeing function'''
    if request.method == "POST":
        q = request.form["q"]
        return redirect(url_for("results", query=q))
    else:
        return render_template("homePage.html")


@app.route("/results?<query>")
def results(query):
    if request.method == "GET":
        return render_template("results.html", q=query)
    else:
        return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        email = request.form['email']
        user = User.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            session['usr'] = user.username
            login_user(user)
            return redirect(url_for('profile'))

    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if User.query.filter_by(email=email).first():
            return "<h1>Email already Present</h1>"
             
        user = User(email=email, username=username, password_hash=None)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("signup.html")


@app.route("/profile")
@login_required
def profile():
    if 'usr' in session:
        usr = session['usr']
        return f"<h1>Welcome {usr}</h1><br><h2><a href='/logout'>Logout Here</a></h2>"
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop('email', None)
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return f"<h1> Oops, you got lost!!</h1><br><h2>{error}</h2>"


if __name__ == "__main__":
    app.run(debug=True)
