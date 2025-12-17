#!/bin/bash
set -e

# 核心：强制导出所有环境变量（修正HIVE_HOME）
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/opt/hadoop-3.3.4
export HIVE_HOME=/opt/apache-hive-3.1.3-bin  # 修正：添加-bin后缀
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin

# 2. 验证命令是否存在（调试用，可保留）
echo "=== Verify Commands ==="
which java
which hadoop
which hive
which schematool
echo "======================="

# Start SSH Service
service ssh start

# Format HDFS (only first run)
if [ ! -d "/opt/hadoop_data/hdfs/namenode/current" ]; then
    hdfs namenode -format
fi

# Start HDFS & YARN
start-dfs.sh
start-yarn.sh

# Create HDFS Directories for Hive
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -mkdir -p /tmp/hive
hdfs dfs -chmod 777 /user/hive/warehouse
hdfs dfs -chmod 777 /tmp/hive

# 3. 修复：使用绝对路径执行schematool（路径已修正）
$HIVE_HOME/bin/schematool -dbType postgres -initSchema

# Start Hive Metastore and Hive Server2（路径已修正）
nohup $HIVE_HOME/bin/hive --service metastore > /var/log/hive-metastore.log 2>&1 &
nohup $HIVE_HOME/bin/hive --service hiveserver2 > /var/log/hive-server2.log 2>&1 &

# Keep Container Running
tail -f /dev/null