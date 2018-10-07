import psycopg2

def main():
    eachrdd_data=[({'repo_name': 'krajj7/BotHack', 'repo_id': '41608f5067f97046f75b0fe1068f0af4f8bf29c8', 'repo_path': 'java/bothack/events/IGameStateHandler.java', 'repo_size': '210', 'class_name': "['no class name']", 'method_names': "['no method name']", 'method_dependencies': "['no method dependencies']"},), ({'repo_name': 'triguero/Keel3.0', 'repo_id': '395da9270d63804deb07abb8b79d1e4038490f1b', 'repo_path':'src/keel/Algorithms/Fuzzy_Rule_Learning/Genetic/ModelFuzzyPittsBurgh/ModelFuzzyPittsBurgh.java', 'repo_size': '10707', 'class_name': "['ModelFuzzyPittsBurgh']", 'method_names': "['fuzzyPittsburghModelling', 'main']", 'method_dependencies': "['String', 'ProcessDataset', 'processModelDataset', 'oldClassificationProcess', 'getNdata', 'getNvariables', 'getNinputs', 'getX', 'getY', 'showDatasetStatistics', 'getImaximum', 'getIminimum', 'getOmaximum', 'getOminimum', 'FuzzyPartition', 'FuzzyModel', 'PittsburghModel', 'setExamples', 'GeneticAlgorithmSteady', 'GeneticAlgorithmGenerational', 'evolve', 'debug', 'trainingResults', 'IOException', 'results', 'catch', 'ProcessConfig', 'fileProcess', 'Randomize', 'setSeed', 'ModelFuzzyPittsBurgh', 'fuzzyPittsburghModelling']"},), ({'repo_name': 'artclarke/xuggle-xuggler', 'repo_id': '4bcc1b59c773abf4ce13c7e6340483dc3b782bf4', 'repo_path': 'src/com/xuggle/mediatool/demos/ModifyAudioAndVideo.java', 'repo_size': '5587', 'class_name': "['TimeStampTool extends', 'VolumeAdjustTool extends']", 'method_names': "['no method name']", 'method_dependencies': "['no method dependencies']"},), ({'repo_name': 'decatur/j2js-compiler', 'repo_id': '95cdf590fc6ad777727966feedde34543bb8013b', 'repo_path': 'src/main/java/com/j2js/assembly/TypeResolver.java', 'repo_size': '2227', 'class_name': "['TypeResolver implements TypeVisitor']", 'method_names': "['TypeResolver', 'visit', 'compile', 'parse']", 'method_dependencies': "['isResolved', 'getLogger', 'getSignature', 'isUpToDate', 'clear', 'compile', 'error', 'printStackTrace', 'debug', 'setResolved', 'getClassFile', 'parse', 'isInterface', 'visit', 'setLastCompiled', 'Parser']"},), ({'repo_name': 'NYRDS/pixel-dungeon-remix', 'repo_id': 'aa2f3082082743e3730f858e5ebcb6b9d5bfe971', 'repo_path': 'PixelDungeon/src/main/java/com/watabou/pixeldungeon/effects/particles/ElmoParticle.java', 'repo_size': '1622', 'class_name': "['ElmoParticle extends PixelParticle.Shrinking']", 'method_names': "['Factory', 'emit', 'lightMode', 'ElmoParticle', 'reset', 'update']", 'method_dependencies': "['recycle', 'color', 'set', 'revive', 'update']"},), ({'repo_name': 'oblac/jodd', 'repo_id': 'f46d3cb739078fdfac54a8f662eddd174a073496', 'repo_path': 'jodd-petite/src/test/java/jodd/petite/tst/Ses.java', 'repo_size': '1797', 'class_name': "['Ses']", 'method_names': "['getValue', 'setValue', 'ciao']", 'method_dependencies': "['no method dependencies']"},), ({'repo_name': 'alibaba/canal', 'repo_id': 'd4ecb07e8d7c3bb3370ae7a724cd625011a6d17f', 'repo_path': 'deployer/src/main/java/com/alibaba/otter/canal/deployer/monitor/SpringInstanceConfigMonitor.java', 'repo_size': '10788', 'class_name': "['SpringInstanceConfigMonitor extends AbstractCanalLifeCycle implements InstanceConfigMonitor, CanalLifeCycle', 'InstanceConfigFiles', 'FileInfo']", 'method_names': "['apply', 'start', 'run', 'stop', 'register', 'unregister', 'setRootConf', 'scan', 'accept', 'accept', 'notifyStart', 'notifyStop', 'notifyReload', 'judgeFileChanged', 'setDefaultAction', 'setScanIntervalInSecond', 'InstanceConfigFiles', 'getDestination', 'setDestination', 'getSpringFile', 'setSpringFile', 'getRootFile', 'setRootFile', 'getInstanceFiles', 'setInstanceFiles', 'FileInfo', 'getName', 'setName', 'getLastModified', 'setLastModified']", 'method_dependencies': "['InstanceConfigFiles', 'start', 'notNull', 'scheduleWithFixedDelay', 'scan', 'error', 'stop', 'shutdownNow', 'clear', 'put', 'remove', 'File', 'exists', 'listFiles', 'getName', 'isDirectory', 'endsWithIgnoreCase', 'equalsIgnoreCase', 'info', 'reload', 'getFullStackTrace', 'lastModified']"},)]

    print(type(eachrdd_data))
    eachrdd_data.foreach(postgres_insert);


def postgres_insert(results):
    #connect postgresql , inorder to insert to table
    # connect postgresql for each worker, inorder to insert to table
    try:
        conn = psycopg2.connect(host="rds-postgresinstance.c5cn8wdvuzrw.us-east-1.rds.amazonaws.com",
                                dbname="mypostgresdb", user="chandra", password="Searchfunction")
    except:
        print("Error in database connection")

    cur = conn.cursor()

    for x in results:
        if (x == ()):
            continue
        else:
            try:  ## insert to postgresql database
                cur.executemany("""INSERT INTO javarepos(repo_name, repo_id, repo_path, repo_size, class_name, method_names, method_dependencies ) \
                         VALUES (%s,%s,%s, %s,%s, %s,%s)""", x)
            except:
                print("Postgres Insertion Error ")
            conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    main()
