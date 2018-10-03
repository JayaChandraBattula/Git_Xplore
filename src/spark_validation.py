from pyspark import SparkContext
from pyspark import SQLContext
import re
import psycopg2

def main():
    sc = SparkContext(master='EC2', appName='Search_Function')
    sqlContext = SQLContext(sc)
    #client = boto3.client('s3',aws_access_key_id = "XXXX", aws_secret_access_key = "XXXXX")
    #s3 = boto3.resource('s3')
    #obj = s3.get_object(Bucket='github-java-sample1', Key='s3://github-java-sample1/github_javarepo5m-000000000000.json')
    #obj = s3.Object(Bucket='github-java-sample1', Key='s3://github-java-sample1/github_javarepo5m-000000000000.json')
    #obj.get()['Body'].read().decode('utf-8')

    for i in range(0,1):
        name_num='{0:03}'.format(i)
        fileName="s3n://*******/github_javarepo5m-000000000"+name_num+".json"
        print(fileName)
        df_rdd=sqlContext.read.json(filename).rdd
        print("File ",fileName," has ",df_rdd.count()," records.")
        df_rdd.foreach(lambda x: data_retrieval(x)).cache()


def data_retrieval(repo_eachrow):
    results=()
    outputdict={}

    try:
        repo_content = repo_eachrow[0]

        repo_id = repo_eachrow[1]
        #print("repo_id",repo_id)
        repo_path = repo_eachrow[2]
        #print("repo_path",repo_path)
        repo_name = repo_eachrow[3]
        #print("repo_name",repo_name)
        repo_size = repo_eachrow[4]
        #print("repo_size", repo_size)
    except:
        return results

    classname_foreachrepo=get_classname(repo_content)
    print("class names",classname_foreachrepo)

    final_outputdict = dict()
    final_outputdict["repo_name"] =str(repo_name)
    final_outputdict["repo_id"] =str(repo_id)
    final_outputdict["repo_path"] =str(repo_path)
    final_outputdict["repo_size"] =str(repo_size)
    final_outputdict["class_name"] = classname_foreachrepo

    #code to insert to the database

def get_classname(each_repo):
    class_name=[]
    str_contentlist=str(each_repo)
    content_list=str_contentlist.split('\n')
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
    return class_name



def get_methodname_dependencies(each_line):

    for line in content_list:
        list1=line.lstrip()
        method_name=''
        tempdict={}
        duplicatedict={}
        duplicatedict.setdefault("Method_Dependencies", [])
        tempdict.setdefault("Method_Name", [])
        tempdict.setdefault("Method_Dependencies", [])

        if ((each_line.startswith('public')) or (each_line.startswith('private')) or (each_line.startswith('protected'))):
            #print(list1)
            try:
                method_name = (str(re.search('\s\w+[(]+', list1).group())[:-1]).lstrip()
                #print(method_name)
                #new_methodname=((str(method_name))[:-1]).lstrip()
                if( (method_name!=None) and ((list1.endswith('{')) or (list1[:-1].endswith('{'))) ):
                    tempdict["Method_Name"].append(method_name)
                    count=1;
            except AttributeError:
                method_name="No methods in this class"
                tempdict["Method_Name"].append(method_name)

        if(count>=1):
            if (count==1 and method_name!=''):
                continue
            for letter in list1:
                if(letter=='{'):
                    count +=1
                    print(" { count ",count)
                elif(letter=='}'):
                    count -=1
                    print(" } count ",count)
                elif(letter=='('):
                    try:
                        dependencies = (str(re.search('\w+[(]+', list1).group())[:-1]).lstrip()
                        #dependencies.append(tempdepend)
                        print("dependencies ",dependencies)
                        if(dependencies!=None):
                            duplicatedict["Method_Dependencies"].append(dependencies)
                            tempdict["Method_Dependencies"].append(set(duplicatedict["Method_Dependencies"]))
                    except AttributeError:
                        dependencies = "No dependencies for the method"
                        duplicatedict["Method_Dependencies"].append(dependencies)
                        tempdict["Method_Dependencies"].append(set(duplicatedict["Method_Dependencies"]))
    return tempdict

if __name__ == "__main__":
     main()
