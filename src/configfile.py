from configparser import ConfigParser

config=ConfigParser()

config['ConfigSparkMain']={
    'debug':'true',
    'url':'jdbc:postgresql://rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com:5432/mypostgresdb',
    'driver': 'org.postgresql.Driver,
    'bucketname': 'github-java-sample1'
    'host': 'ec2-52-6-184-3.compute-1.amazonaws.com'
    'port':80
}


config['params'] = {
    'database': 'mypostgresdb',
    'user': 'chandra',
    'password': 'Searchfunction',
    'host': 'jdbc:postgresql://rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com',
    'port': 5432
}

with open('./parse.ini','w') as f:
    config.write(f)
