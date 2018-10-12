from flask import render_template, request, flash, url_for, redirect
from flask import Flask
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor


app = Flask('Git Xplore') #creating a flask app git xplore

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

#routing to home.html page
@app.route("/")
@app.route("/home")
def home():
    title = 'Home'
    return render_template('home.html', title=title)

#routing to getdata page where information is queried based on the input entered in the page
#and the out is rendered to view.html page
@app.route("/getdata", methods=["GET", "POST"])
def getdata():
    repoid = request.form['repo_id']
    reponame = request.form['repo_name']
    print("repo name ",reponame)
    classname = request.form['class_name']
    print("class name ",classname)
    methodnames = request.form['method_names']
    print("Method name ",methodnames)
    cur = conn.cursor()

    if(not reponame and not classname):
        results=[]
        print("results ",results)
        return render_template('view.html', results=results)
    elif(reponame != None and classname!=None):
        print("in both repo name and class name")
        likeString1 = "%" + reponame + "%"
        print("likeString1 in reponame",likeString1)
        likeString2 = "%" + classname + "%"
        print("likeString2 in class",likeString2)
        # get data from table 'total'
        cur.execute("SELECT *\
                       FROM javarepos \
                      WHERE repo_name iLIKE %s AND class_name iLIKE %s;",\
                       (likeString1, likeString2))
        print("after cur.exe")
        results=cur.fetchall()
        print("results ",results)
        return render_template('view.html', results=results)
    elif(reponame != None and classname==None):
        print("in both repo name ")
        likeString1 = "%" + reponame + "%"
        print("likeString1 in reponame",likeString1)
        # get data from table 'total'
        cur.execute("SELECT *\
                       FROM javarepos \
                      WHERE repo_name iLIKE %s;",\
                       (likeString1))
        print("after cur.exe")
        results=cur.fetchall()
        print("results ",results)
        return render_template('view.html', results=results)
    elif(reponame == None and classname!=None):
        print("in class name")
        likeString1 = "%" + classname + "%"
        print("likeString1 in classname",likeString1)
        # get data from table 'total'
        cur.execute("SELECT *\
                       FROM javarepos \
                      WHERE class_name iLIKE %s;",\
                       (likeString1))
        print("after cur.exe")
        results=cur.fetchall()
        print("results ",results)
        return render_template('view.html', results=results)
    else:
        results=[]
        print("results ",results)
        return render_template('view.html', results=results)


@app.route("/about")
def about():
    title = 'About'
    return render_template('about.html', title=title)

if (__name__ == "__main__"):
    app.run(host='ec2-52-6-184-3.compute-1.amazonaws.com',debug='true')
