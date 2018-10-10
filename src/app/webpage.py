from flask import Flask
from flask import *
from flask import render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extras import RealDictCursor
import psycopg2
import pandas as pd

app = Flask(__name__)

POSTGRES = {
    'user': 'chandra',
    'pw': 'Searchfunction',
    'db': 'mypostgresdb',
    'host': 'rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db=SQLAlchemy(app)


@app.route("/home", methods=["GET", "POST"])
def home():
    if flask.request.method == 'POST':
         print("in post")
         reponame = flask.request.values.get('repo_name') # Your form's
         print("reponame ",reponame)
         classname = flask.request.values.get('class_name') # input names
         class_name = request.form['class_name']
         print("class name 2",class_name)
    try:
        conn = psycopg2.connect(**POSTGRES)
    except Exception as er:
        print("Unable to connect to the database")
        print(str(er))

    cur = conn.cursor(cursor_factory=RealDictCursor)

    if (repo_name!= null and class_name!=null):
        # get data from table 'javarepos'
        cur.execute("SELECT * \
                       FROM total \
                      WHERE class_name like 'class_name' AND  repo_name like 'repo_name'" )
        rec=cur.fetchall()
        rows=rec.result()
        df=pd.DataFrame(list(rows))
    cur.close()
    conn.close()
    return render_template('home.html',table=df.to_html(classes='QueryResult'))

@app.route("/about")
def about():
    title='About'
    return render_template('about.html',title=title)

if (__name__ == "__main__"):
    app.run(host='ec2-52-6-184-3.compute-1.amazonaws.com',debug='true')
