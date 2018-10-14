# Installing necessary packages on the cluster to run spark jobs

### 1) Starting cluster
export AWS_ACCESS_KEY_ID=XXXX
export AWS_SECRET_ACCESS_KEY=XXXX
export AWS_DEFAULT_REGION=us-east-1
export REM_USER=ubuntu
$source ~/.bash_profile
$peg fetch <cluster-name>
---finds the .pem file in the local and adds them to ssh-agent
$peg start <cluster-name>
all the instances in the aws will be started(if in stopped state)

### 2) Installing spark on cluster
$peg install <cluster-name> spark (installs spark on the cluster; all nodes)

### 3) Start hadoop and spark on the cluster
$peg service <cluster-name> hadoop start
$peg service <cluster-name> spark start

### 4) ssh into the cluster master node
$peg ssh <cluster-name> <master-node-number>

### 5) Install all required software's on the cluster
$pip install pyspark
$pip install psycopg2
$pip install Git
$pip install Flask

### 6)submitting spark jobs (navigate to the source folder which contains the .py file, add needed jars )
${SPARK_HOME}/bin/spark-submit --master spark://ec2-52-6-184-3.compute-1.amazonaws.com:7077
                                --jars /home/ubuntu/postgresql-42.2.5.jar spark_validation.py

### 7) spark jobs can be monitored with the help of spark WebUI
http:/XXXXXX.compute-1.amazonaws.com:8080 (master node public dns with port number)

### 8) Adjust security groups such that they allow traffic for the ports and ips you use.
