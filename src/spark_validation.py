from pyspark import SparkContext
from pyspark import SQLContext
import pandas as pd
import re

def data_retrieval(filename)
    content_list=[]
    content_list=filename.split('\n')
    print("total number of lines: ",len(content_list))

    outputdict={}
    class_name=''
    outputdict.setdefault("Class_Name", [])
    method_name=''
    outputdict.setdefault("Method_Name", [])

    for line in content_list:
        list1=line.lstrip()

        # retrieving class information
        if ((list1.startswith('public')) or (list1.startswith('private')) or (list1.startswith('static'))):
            #print("lines with public keyword ",list1)
            try:
                #print("in try block")
                start = ' class '
                end = ' '
                class_name = re.search('%s(.*)%s' % (start,end), list1).group(1)
                #print(type(class_name))
                #print(class_name)
                outputdict["Class_Name"].append(str(class_name))
            except AttributeError:
                print("No class name found")

        # retrieving method information
        if ((list1.startswith('public')) or (list1.startswith('private')) or (list1.startswith('protected'))):
           #print("lines with public keyword ",list1)
           try:
               #print("in try block")
               method_name = re.search('\s\w+[(]+', list1).group()
               #print((str(method_name))[:-1])
               outputdict["Method_Name"].append(((str(method_name))[:-1]).lstrip())
            except AttributeError:
               print("No method name found")

    for k, v in outputdict.items():
		print(v)

    return outputdict

def read_jsonfile_fromS3(filename):
    df_json = sqlContext.read.json(filename)
    df_json.registerTempTable("tempTable")
    df_json_rdd=sqlContext.sql("SELECT id, repo_name, path, size, content FROM tempTable where content != ''").rdd
    return df_json_rdd


def main():
    sc = SparkContext(master='local', appName='demo')
    sqlContext = SQLContext(sc)

    filename = "s3a://bucketname".json"
    df_rdd=read_jsonfile_fromS3(filename)

    output_values = ()
    output_values = df_rdd.map(lambda x: data_retrieval(x))
