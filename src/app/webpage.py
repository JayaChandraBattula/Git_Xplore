from flask import render_template, request, flash, url_for, redirect
from flask import Flask


app = Flask('Git Xplore')


@app.route("/")
@app.route("/home")
def home():
    title = 'Home'
    return render_template('home.html', title=title)
