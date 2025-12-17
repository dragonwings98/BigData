# 基础镜像：Ubuntu 22.04（稳定且兼容Spark）
FROM ubuntu:22.04

# 设置环境变量，避免交互提示
ENV DEBIAN_FRONTEND=noninteractive
# Spark 版本和安装路径
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# 安装依赖：Java（Spark 必需）、Python3、pip、wget、解压工具
RUN apt update && apt install -y \
    openjdk-11-jdk \
    python3 \
    python3-pip \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# 软链接 python -> python3（统一命令）
RUN ln -s /usr/bin/python3 /usr/bin/python

# 下载并解压 Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt/ \
    && mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# 设置工作目录
WORKDIR /opt/spark/work-dir

# 暴露 Spark UI 端口（可选，用于访问监控界面）
EXPOSE 4040 7077 8080

# 启动时进入bash（方便交互）
CMD ["bash"]