from flask import render_template, request, flash, url_for, redirect
from flask import Flask


app = Flask('Git Xplore')


@app.route("/")
@app.route("/home")
def home():
    title = 'Home'
    return render_template('home.html', title=title)

if (__name__ == "__main__"):
    app.run(host='ec2-52-6-184-3.compute-1.amazonaws.com',debug='true')
