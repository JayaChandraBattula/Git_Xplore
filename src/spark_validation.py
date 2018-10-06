from pyspark import SparkContext
from pyspark import SQLContext
import re
import psycopg2

def main():
    sc = SparkContext( appName='Search_Function')
    sqlContext = SQLContext(sc)
    #client = boto3.client('s3',aws_access_key_id = "XXXX", aws_secret_access_key = "XXXXX")
    #s3 = boto3.resource('s3')
    #obj = s3.get_object(Bucket='github-java-sample1', Key='s3://github-java-sample1/github_javarepo5m-000000000000.json')
    #obj = s3.Object(Bucket='github-java-sample1', Key='s3://github-java-sample1/github_javarepo5m-000000000000.json')
    #obj.get()['Body'].read().decode('utf-8')

    for i in range(0,1):
        name_num='{0:03}'.format(i)
        fileName="s3a://github-java-sample1/github_javarepo5m-000000000"+name_num+".json"
        print(fileName)
        df_rdd=sqlContext.read.json(fileName).rdd
        print("File ",fileName," has ",df_rdd.count()," records.")
        eachrdd_data=()
        eachrdd_data=df_rdd.foreach(lambda x: data_retrieval(x))
        eachrdd_data.foreachrdd(postgres_insert)

def data_retrieval(repo_eachrow):
    results=()
    outputdict={}

    try:
        repo_content = repo_eachrow[0].encode('ascii','ignore').decode('ascii')

        repo_id = repo_eachrow[1].encode('ascii','ignore').decode('ascii')
        print("repo_id",repo_id)
        repo_path = repo_eachrow[2].encode('ascii','ignore').decode('ascii')
        print("repo_path",repo_path)
        repo_name = repo_eachrow[3].encode('ascii','ignore').decode('ascii')
        print("repo_name",repo_name)
        repo_size = repo_eachrow[4].encode('ascii','ignore').decode('ascii')
        print("repo_size", repo_size)
    except:
        return results({'repo_name': 'no repo name', 'repo_id': 'no repo id', 'repo_path': 'no repo path', 'repo_size': '00',
                        'class_name': ['no class name'], 'method_names': ['no method names'], 'method_dependencies': ['no method dependencies']},)


    str_contentlist = str(repo_content)
    classname_foreachrepo=get_classname(str_contentlist)
    methodname_foreachrepo,methoddependencies_foreachrepo=get_methodname_dependencies(str_contentlist)


    final_outputdict = dict()
    final_outputdict["repo_name"] =str(repo_name)
    final_outputdict["repo_id"] =str(repo_id)
    final_outputdict["repo_path"] =str(repo_path)
    final_outputdict["repo_size"] =str(repo_size)
    final_outputdict["class_name"] = classname_foreachrepo
    final_outputdict["method_names"] = methodname_foreachrepo
    final_outputdict["method_dependencies"] = methoddependencies_foreachrepo

    results=results +(final_outputdict,)

    print(results)

    return results


def postgres_insert(results):
    #connect postgresql for each worker, inorder to insert to table
    try:
        conn = psycopg2.connect(host="rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com",
                                dbname="mypostgresdb",user="chandra", password="Searchfunction")
    except:
        print("Error in database connection")

    cur = conn.cursor()

    for x in results:
        # insert to postgresql database
        try:
            cur.executemany("INSERT INTO javarepos(repo_name, repo_id, repo_path, repo_size, class_name, method_names, method_dependencies ) \
                 VALUES (%s,%s,%s, %s,%s, %s,%s)
        except:
            print("Postgres Insertion Error ")
        conn.commit()
        cur.close()

        conn.close()

def get_classname(each_repo):
    class_name=[]
    content_list=each_repo.split('\n')
    print("length of content list for a row",len(content_list))
    for line in content_list:
        each_line=line.lstrip()
        if ((each_line.startswith('public')) or (each_line.startswith('private')) or (each_line.startswith('static'))):
            try:
                start = ' class '
                end = ' '
                class_name.append(re.search('%s(.*)%s'% (start,end), each_line).group(1))
            except AttributeError:
                continue
    if not class_name:
        class_name.append('no class name')
    return class_name


def get_methodname_dependencies(each_repo):
    content_list = each_repo.split('\n')
    methodname_list = []
    methoddependencies_list = []
    count = 0

    for line in content_list:
        method_name = ''
        each_line = line.lstrip()

        if ((each_line.startswith('public')) or (each_line.startswith('private')) or (
        each_line.startswith('protected'))):
            try:
                method_name = (str(re.search('\s\w+[(]+', each_line).group())[:-1]).lstrip()
                if ((method_name != None) and ((each_line.endswith('{')) or (each_line[:-1].endswith('{')))):
                    methodname_list.append(method_name)
                    count = 1
            except AttributeError:
                continue

        if (count >= 1):
            if (count == 1 and method_name != ''):
                continue
            for letter in each_line:
                if (letter == '{'):
                    count += 1
                elif (letter == '}'):
                    count -= 1
                elif (letter == '('):
                    try:
                        method_dependencies = str(re.search('\w+[(]+', each_line).group())[:-1].lstrip()
                        if (method_dependencies != None and method_dependencies not in methoddependencies_list
                                and method_dependencies not in ['println', 'get']):
                            methoddependencies_list.append(method_dependencies)
                    except AttributeError:
                        continue
                else:
                    continue
    if not methodname_list:
        methodname_list.append('no method name')
    if not methoddependencies_list:
        methoddependencies_list.append('no method dependencies')
    return (methodname_list,methoddependencies_list)


if __name__ == "__main__":
     main()
