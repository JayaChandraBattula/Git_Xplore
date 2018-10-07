import psycopg2

def main():
    #connect postgresql , inorder to insert to table
    try:
        conn = psycopg2.connect(host="XX",
                               dbname="mypostgresdb",user="chandra", password="Searchfunction")
        # Create table
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS javarepos(
            repo_id text,
            repo_name text,
            repo_path text,
            repo_size text,
            class_name text[],
            method_names text[],
            method_dependencies text[]
        )
        """)

        cur.execute("""
        INSERT INTO javarepos (repo_id, repo_name,repo_path,repo_size,class_name,method_names,method_dependencies)
        VALUES
              ('drfgfhfjsdhuerrhr8498t438fseh3', 'chandfdsra/searchfunctioreeegsdn','https://github.com/JayaChandraBathula/search_functidgrgon','445355','{"fersfgrdsrdv","fscrtererg","csdcefgdtbrgb"}','{"iusrvugttreiv"}','{"vhevftgdrfbier"}')
        """)

        conn.commit()
        cur.close()
        conn.close()

    except:
        print "unable to connect to the database."



if __name__ == '__main__':
    main()
