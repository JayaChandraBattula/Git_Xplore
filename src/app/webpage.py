from flask import render_template, request, flash, url_for, redirect
from flask import Flask
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor


app = Flask('Git Xplore')

# parameters for postgres database connection
params = {
    'database': 'mypostgresdb',
    'user': 'chandra',
    'password': 'Searchfunction',
    'host': 'rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com',
    'port': 5432
}

try:
    conn = psycopg2.connect(**params)
except Exception as er:
        print("Unable to connect to the database")
        print(str(er))


@app.route("/")
@app.route("/home")
def home():
    title = 'Home'
    return render_template('home.html', title=title)


@app.route("/getdata", methods=["GET", "POST"])
def getdata():
    repoid = request.form['repo_id']
    reponame = request.form['repo_name']
    print("repo name ",reponame)
    classname = request.form['class_name']
    print("class name ",classname)
    methodnames = request.form['method_names']

    #cur = conn.cursor(cursor_factory=RealDictCursor)
    cur = conn.cursor()

    # if (reponame != None):
    #     likeString1 = "'%%" + reponame + "%%'"
    #     print("likeString1 ",likeString1)
    #     likeString2 = "'%%" + classname + "%%'"
    #     print("likeString2 ",likeString2)
    #     # get data from table 'total'
    #     cur.execute("SELECT *\
    #                    FROM javarepos \
    #                   WHERE repo_name = %s",\
    #                    (reponame))
    #     print("after cur.exe")
    #     results=cur.fetchall()
    #     print("results ",results)
    #     return render_template('view.html', repoinfo=results)


    if (reponame != None and classname!=None):
        likeString1 = "'%" + reponame + "%'"
        print("likeString1 ",likeString1)
        likeString2 = "'%" + classname + "%'"
        print("likeString2 ",likeString2)
        # get data from table 'total'
        cur.execute("SELECT *\
                       FROM javarepos \
                      WHERE repo_name like %s AND class_name like %s;",\
                       (likeString1, likeString2))




@app.route("/about")
def about():
    title = 'About'
    return render_template('about.html', title=title)

if (__name__ == "__main__"):
    app.run(host='ec2-52-6-184-3.compute-1.amazonaws.com',debug='true')
