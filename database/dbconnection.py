import psycopg2

def main():
    #connect postgresql , inorder to insert to table
    try:
        conn = psycopg2.connect(host="*********************************************",
                                dbname="mypostgresdb",user="chandra", password="Searchfunction")
        # Create table
        cur = conn.cursor()
        cur.execute("
        CREATE TABLE IF NOT EXISTS javarepos(
            repo_id text PRIMARY KEY,
            repo_name text,
            repo_path text,
            repo_size text,
            class_name text[],
            method_name text[],
            method_dependencies text[],
        )
        ")
        cur.executemany("INSERT INTO javarepos(repo_name, repo_id, repo_path, repo_size, class_name, method_names, method_dependencies ) \
                 VALUES ()

        conn.commit()
        conn.close()

    except:
         print "unable to connect to the database."



if __name__ == '__main__':
    main()
