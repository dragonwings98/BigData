# HW1

Build the image

​`cd`

​`docker build -t hadoop-3.3.6:task .`

![image](assets/image-20251216004426-1lj6658.png)

run docker

![image](assets/image-20251216004454-7zej74j.png)

HDFS and YARN services failed to start successfully

```bash
# Start the SSH service
service ssh start

# Verify if SSH is started
ps -ef | grep sshd  # If you can see the sshd process, it means success.

cd $HADOOP_HOME/etc/hadoop

# 2. Fix hadoop-env.sh (add the missing environment variables)
echo "export HDFS_NAMENODE_USER=\"root\"" >> hadoop-env.sh
echo "export HDFS_DATANODE_USER=\"root\"" >> hadoop-env.sh
echo "export HDFS_SECONDARYNAMENODE_USER=\"root\"" >> hadoop-env.sh
echo "export YARN_RESOURCEMANAGER_USER=\"root\"" >> hadoop-env.sh
echo "export YARN_NODEMANAGER_USER=\"root\"" >> hadoop-env.sh

# 3. Reformat HDFS (force overwrite)
hdfs namenode -format -force

# Start HDFS
start-dfs.sh

jps  # At this point, you should see NameNode, DataNode, and SecondaryNameNode.

# Start YARN
start-yarn.sh

jps
```

![image](assets/image-20251216004605-qvmm8vs.png)

task 1 Создайте директорию на HDFS /createme

​`hdfs dfs -mkdir /createme`

![image](assets/image-20251216004849-3lvzts3.png)

task 2 Удалите директорию на HDFS /delme

![image](assets/image-20251216005015-yf1oadk.png)

task3 Создайте файл на HDFS /nonnull.txt с произвольным содержимым:

![image](assets/image-20251216005407-nno9q8i.png)

task4 Выполните джобу MR wordcount через YARN для файла /shadow.txt

submit shadow.txt in docker

![image](assets/image-20251216010148-ba6yf9e.png)

Rewrite the complete mapred-site.xml

```bash
echo '<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
    <property>
        <name>mapreduce.map.env</name>
        <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
    <property>
        <name>mapreduce.reduce.env</name>
        <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
</configuration>' > $HADOOP_CONF_DIR/mapred-site.xml

stop-yarn.sh

start-yarn.sh
```

Execute the WordCount task

​`hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /shadow.txt /wordcount-output`

Verify the WordCount results

​`hdfs dfs -cat /wordcount-output/part-r-00000`![image](assets/image-20251216010830-kp184lq.png)

task5 Запишите число вхождений слова "Innsmouth" в файл /whataboutinsmouth.txt

​`count=$(hdfs dfs -cat /shadow.txt | grep -o "Innsmouth" | wc -l)`

​`echo $count | hdfs dfs -put - /whataboutinsmouth.txt`

![image](assets/image-20251216010938-ggmdo98.png)
