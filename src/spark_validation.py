from pyspark import SparkContext
from pyspark import SQLContext
import re
import psycopg2

def main():
    sc = SparkContext( appName='Git_Xplore') # creating spark Context for the app Git Xplore
    sqlContext = SQLContext(sc)

    #Iterating through each file and writing to postgres database
    for i in range(0,1):
        name_num='{0:03}'.format(i)
        fileName="s3a://github-java-sample1/github_javarepo5m-000000000"+name_num+".json"
        eachfile_rdd=sqlContext.read.json(fileName).rdd
        print("File ",fileName," has ",eachfile_rdd.count()," records.")
        eachrdd_data=eachfile_rdd.map(lambda x: data_retrieval(x))
        hasattr(eachrdd_data,"toDF")
        df=eachrdd_data.toDF(schema=['repo_name', 'repo_id', 'repo_path', 'repo_size',
                        'class_name', 'method_names', 'method_dependencies'])

        df=df.na.drop(thresh=7)
        df.show()
        url="jdbc:postgresql://rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com:5432/mypostgresdb"
        properties = {"user": "chandra","password": "Searchfunction","driver": "org.postgresql.Driver"}
        df.write.mode('append').jdbc(url=url, table="javarepos",properties =properties )


# Passing each repo through data_retrieval method and returning the class and method names and their dependencies
def data_retrieval(repo_eachrow):
    results=()
    outputdict={}

    try:
        repo_content = repo_eachrow[0].encode('ascii','ignore').decode('ascii')
        repo_id = repo_eachrow[1].encode('ascii','ignore').decode('ascii')
        repo_path = repo_eachrow[2].encode('ascii','ignore').decode('ascii')
        repo_name = repo_eachrow[3].encode('ascii','ignore').decode('ascii')
        repo_size = repo_eachrow[4].encode('ascii','ignore').decode('ascii')
    except:
        return results

    str_contentlist = str(repo_content)
    classname_foreachrepo=get_classname(str_contentlist)
    methodname_foreachrepo,methoddependencies_foreachrepo=get_methodname_dependencies(str_contentlist)

    temptuple=(repo_name,repo_id,repo_path,repo_size,str(classname_foreachrepo),str(methodname_foreachrepo),str(methoddependencies_foreachrepo))

    results=results +temptuple
    print(results)
    return results

# Getting class names from each repo
def get_classname(each_repo):
    class_name=set()
    content_list=each_repo.split('\n')
    print("length of content list for a row",len(content_list))
    for line in content_list:
        each_line=line.lstrip()
        if ((each_line.startswith('public')) or (each_line.startswith('private')) or (each_line.startswith('static'))):
            try:
                start = ' class '
                end = ' '
                class_name.add(re.search('%s(.*)%s'% (start,end), each_line).group(1))
            except AttributeError:
                continue
    if not class_name:
        class_name.add("no class name")
    return class_name


# Getting method names from each repo
def get_methodname_dependencies(each_repo):
    content_list = each_repo.split('\n')
    methodname_set = set()
    methoddependencies_set = set()
    count = 0

    for line in content_list:
        method_name = ""
        each_line = line.lstrip()

        if ((each_line.startswith('public')) or (each_line.startswith('private')) or (
        each_line.startswith('protected'))):
            try:
                method_name = (str(re.search('\s\w+[(]+', each_line).group())[:-1]).lstrip()
                if ((method_name != None) and ((each_line.endswith('{')) or (each_line[:-1].endswith('{')))):
                    methodname_set.add(method_name)
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
                        if (method_dependencies != None and method_dependencies not in methoddependencies_set
                                and method_dependencies not in ['println', 'get']):
                            methoddependencies_set.add(method_dependencies)
                    except AttributeError:
                        continue
                else:
                    continue
    if not methodname_set:
        methodname_set.add("no method name")
    if not methoddependencies_set:
        methoddependencies_set.add("no method dependencies")
    return (methodname_set,methoddependencies_set)



if __name__ == "__main__":
     main()
