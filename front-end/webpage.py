from flask import Flask
from flask import render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from app import db
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


@app.route("/about")
def about():
    title='About'
    return render_template('about.html',title=title)

@app.route("/webhome_getdata", methods=["GET", "POST"])
def webhome_getdata():
    repo_name = request.form['repo_name']
    class_name = request.form['class_name']

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
    return render_template('view.html',table=df.to_html(classes='QueryResult'))


if (__name__ == "__main__"):
app.run()
