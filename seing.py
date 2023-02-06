#! /usr/bin/env python

from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def home():
    '''Homepage routeing function'''
    return render_template("homePage.html")


if __name__ == "__main__":
    app.run(debug=True)
