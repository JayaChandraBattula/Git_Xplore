#!/usr/bin/env bash


# Run script to process files on ec2 spark cluster

${SPARK_HOME}/bin/spark-submit --master spark://ec2-52-6-184-3.compute-1.amazonaws.com:7077
                                  --jars /home/ubuntu/postgresql-42.2.5.jar spark_validation.py
