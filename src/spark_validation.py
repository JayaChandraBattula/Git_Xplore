from pyspark import SparkContext
from pyspark import SQLContext
import re
import psycopg2




def read_jsonfile_fromS3(filename):
    df_json = sqlContext.read.json(filename)
    df_json.registerTempTable("tempTable")
    df_json_rdd=sqlContext.sql("SELECT id, repo_name, path, size, content FROM tempTable where content != ''").rdd
    return df_json_rdd




def data_retrieval(repo_eachrow):
    results=()
    outputdict={}

    try:
        repo_name = repo[0].encode('ascii','ignore')
        repo_id = repo[1].encode('ascii','ignore')
        repo_path = repo[2].encode('ascii','ignore')
        repo_size = repo[3].encode('ascii','ignore')
        repo_content = repo[4].encode('ascii','ignore')
    except:
        return results

    content_list=repo_content.split('\n')

    if(len(content_list)<=1):
        return results

    class_name=get_classname(content_list)
    method_name=get_methodname(content_list)

    final_outputdict = dict()
    final_outputdict["repo_name"] =str(repo_name)
    final_outputdict["repo_id"] =str(repo_id)
    final_outputdict["repo_path"] =str(repo_path)
    final_outputdict["repo_size"] =str(repo_size)
    final_outputdict["class_name"] =str(class_name)
    final_outputdict["method_name"] =method_name.get_methodname  ## to get method name values
    final_outputdict["method_dependencies"] =method_name.get_methodname_dependencies  ## to get method name values

    # results declaration

def get_classname(each_repo):
    for line in content_list:
        list1=line.lstrip()
        if ((each_repo.startswith('public')) or (each_repo.startswith('private')) or (each_repo.startswith('static'))):
            try:
                start = ' class '
                end = ' '
                class_name = re.search('%s(.*)%s' % (start,end), list1).group()
                #outputdict["Class_Name"].append(str(class_name))
            except AttributeError:
                #outputdict["Class_Name"].append(str(class_name))
                class_name="no class is present"
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




def main():
    sc = SparkContext(master='EC2', appName='Search_Function')
    sqlContext = SQLContext(sc)
    client = boto3.client('s3',aws_access_key_id = "XXXX", aws_secret_access_key = "XXXXX")

    for i in range(0,5):
        name_num='{0:01}'.format(i)
        fileName="s3a://*******/*******-000000000"+name_num+".json"
        df_rdd=read_jsonfile_fromS3(filename)
        print("File "+fileName+" has "+df_rdd.count()+" records.")

    output_values = ()
    output_values = df_rdd.map(lambda x: data_retrieval(x))



if __name__ == "__main__":
     main()
