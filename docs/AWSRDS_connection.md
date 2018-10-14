### Connect to AWS RDS PostgreSQL database

1. launch an AWS RDS instance
2. install `psycopgs` on every node of spark-cluster
    ```
    pip install psycopg2-binary
    ```
3. all connection parameters
    - master-username,
    - password,
    - endpoint,
    - port (5432)
4. run the following example python codes
    ```python
    import psycopg2
    params = {
        'database': database name,
        'user': '****',
        'password': '*****',
        'host': endpoint,
        'port': 5432
    }
    try:
        conn = psycopg2.connect(**params)
    except Exception as er:
        print(str(er))
    cur = conn.cursor()
    # create table
    cur.execute("CREATE TABLE IF NOT EXISTS test (XXXXXXXXX);")
    cur.close()
    conn.close()
    ```
5. configure security groups in aws to allow inbound traffic and outbound traffic for data write and read
