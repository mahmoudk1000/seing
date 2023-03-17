#! /usr/bin/env python

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
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
        return redirect(url_for("/"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.errorhandler(404)
def page_not_found(error):
    return f"<h1> Oops, you got lost!!</h1><br><h2>{error}</h2>"


if __name__ == "__main__":
    app.run(debug=True)
