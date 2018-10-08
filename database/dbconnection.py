import psycopg2

def main():
    eachrdd_data=[({'repo_name': 'krajj7/BotHack', 'repo_id': '41608f5067f97046f75b0fe1068f0af4f8bf29c8', 'repo_path': 'java/bothack/events/IGameStateHandler.java', 'repo_size': '210', 'class_name': "['no class name']", 'method_names': "['no method name']", 'method_dependencies': "['no method dependencies']"},),]
    #('krajj7/BotHack', '41608f5067f97046f75b0fe1068f0af4f8bf29c8', 'java/bothack/events/IGameStateHandler.java','210',"['no class name']",  "['no method name']",  "['no method dependencies']")
    print(type(eachrdd_data))
    eachrdd_data.foreach(postgres_insert);


def postgres_insert(results):
    #connect postgresql , inorder to insert to table
    # connect postgresql for each worker, inorder to insert to table
    try:
        conn = psycopg2.connect(host="rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com",
                                dbname="mypostgresdb", user="chandra", password="Searchfunction")
    except:
        print("Error in database connection")

    cur = conn.cursor()

    for x in results:
        if (x == ()):
            continue
        else:
            try:  ## insert to postgresql database
                cur.executemany("""INSERT INTO javarepos(repo_name, repo_id, repo_path, repo_size, class_name, method_names, method_dependencies ) \
                         VALUES (%s,%s,%s, %s,%s, %(method_names)s,%(method_dependencies)s)""", x)
            except:
                print("Postgres Insertion Error ")
            conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    main()
