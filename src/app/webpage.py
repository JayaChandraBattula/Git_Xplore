import flask
from flask import Flask
from flask import *
from flask import render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from psycopg2.extras import RealDictCursor
import psycopg2
import pandas as pd
from sqlalchemy import and_

#app = flask.Flask('GitXplore')

# POSTGRES = {
#     'user': 'chandra',
#     'pw': 'Searchfunction',
#     'db': 'mypostgresdb',
#     'host': 'rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com',
#     'port': '5432',
# }
#
print("started")
app = Flask('GitXplore')
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chandra:Searchfunction@rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com:5432/mypostgresdb'
except:
    print("exception")

db=SQLAlchemy(app)

@app.route("/start")
def start():
    title='Home page'
    return render_template('home.html',title=title)

@app.route('/home', methods=["POST"])
def home():
    repoinfo=javarepos(request.form['repo_name'],
                            request.form['class_name'])
    repo_name=repoinfo.repo_name
    class_name=repoinfo.class_name
    resultset=query.filter_by(javarepos.repo_name.like('%repo_name%')).filter_by(javarepos.class_name.like('%class_name%')).all()
    return render_template('view.html',resultset=resultset)

    #repoquery=javarepos.query.filter_by(repo_name=repoinfo.repo_name,class_name=repoinfo.class_name).first()


    #db.session.add(repoinfo)
    #db.session.commit()



    # if flask.request.method == 'POST':
    #      print("in post")
    #      reponame = flask.request.values.get('repo_name') # Your form's
    #      print("reponame ",reponame)
    #      classname = flask.request.values.get('class_name') # input names
    #      class_name = request.form['class_name']
    #      print("class name 2",class_name)
    # try:
    #     conn = psycopg2.connect(host="rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com:5432/mypostgresdb",
    #             user="chandra", password="Searchfunction")
    # except Exception as er:
    #     print("Unable to connect to the database")
    #     print(str(er))
    #
    # cur = conn.cursor(cursor_factory=RealDictCursor)
    #
    # if (repo_name!= null and class_name!=null):
    #     # get data from table 'javarepos'
    #     cur.execute("SELECT * \
    #                    FROM total \
    #                   WHERE class_name like 'class_name' AND  repo_name like 'repo_name'" )
    #     rec=cur.fetchall()
    #     rows=rec.result()
    #     df=pd.DataFrame(list(rows))
    # cur.close()
    # conn.close()
    # return render_template('home.html',table=df.to_html(classes='QueryResult'))

@app.route("/about")
def about():
    title='About'
    return render_template('about.html',title=title)

if (__name__ == "__main__"):
    app.run(host='localhost',debug='true')
    # app.run(host='ec2-52-6-184-3.compute-1.amazonaws.com',debug='true')
