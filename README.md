# Hadoop 3.3.6 Multinode Cluster Setup Using WSL2, OpenJDK 11, Docker, and Docker Compose
This guide provides step-by-step instructions to set up a Hadoop 3.3.6 multinode cluster using WSL2, OpenJDK 11 in Docker containers, orchestrated with Docker Compose.

## Prerequisites
* WSL2 enabled on your system
* Docker and Docker Compose installed
* Basic understanding of Docker and Hadoop

## Setup
1. Create the Docker Network
Create a Docker network to allow communication between the Hadoop cluster containers.

```shell
docker network create hadoop_network
```

2. Build the Base Docker Image
Create a Dockerfile for the Hadoop base image.

```dockerfile
# Use the official OpenJDK 11 image as the base for the build
FROM openjdk:11-jdk AS jdk

# Use the official Python 3.11 image
FROM python:3.11

USER root

# --------------------------------------------------------
# JAVA
# --------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-launchpadlib \
    software-properties-common && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the JAVA_HOME environment variable for the AMD64 architecture
ENV JAVA_HOME=/usr/local/openjdk-11

# Copy OpenJDK from the first stage
COPY --from=jdk $JAVA_HOME $JAVA_HOME

# --------------------------------------------------------
# HADOOP
# --------------------------------------------------------
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_URL=https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
ENV HADOOP_PREFIX=/opt/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV MULTIHOMED_NETWORK=1
ENV USER=root
ENV HADOOP_HOME=/opt/hadoop-$HADOOP_VERSION
ENV PATH $HADOOP_PREFIX/bin/:$PATH
ENV PATH $HADOOP_HOME/bin/:$PATH

RUN set -x \
    && curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz \
    && tar -xvf /tmp/hadoop.tar.gz -C /opt/ \
    && rm /tmp/hadoop.tar.gz*

RUN ln -s /opt/hadoop-$HADOOP_VERSION/etc/hadoop /etc/hadoop
RUN mkdir /opt/hadoop-$HADOOP_VERSION/logs
RUN mkdir /hadoop-data

USER root

COPY conf/core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY conf/hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml
COPY conf/mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
COPY conf/yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml
```

Build the Docker image.

```shell
docker build -t hadoop-base:3.3.6 .
```

3. Create Docker Compose File
Create a docker-compose.yml file to define the Hadoop services.

```yaml
version: "2.4"

services:
  namenode:
    build: ./namenode
    container_name: namenode
    volumes:
      - hadoop_namenode:/hadoop/dfs/name
      - ./data/:/hadoop-data/input
      - ./map_reduce/:/hadoop-data/map_reduce
    environment:
      - CLUSTER_NAME=test
    ports:
      - "9870:9870"
      - "8020:8020"
    networks:
      - hadoop_network

  resourcemanager:
    build: ./resourcemanager
    container_name: resourcemanager
    restart: on-failure
    depends_on:
      - namenode
      - datanode1
      - datanode2
      - datanode3
    ports:
      - "8089:8088"
    networks:
      - hadoop_network

  historyserver:
    build: ./historyserver
    container_name: historyserver
    depends_on:
      - namenode
      - datanode1
      - datanode2
    volumes:
      - hadoop_historyserver:/hadoop/yarn/timeline
    ports:
      - "8188:8188"
    networks:
      - hadoop_network

  nodemanager1:
    build: ./nodemanager
    container_name: nodemanager1
    depends_on:
      - namenode
      - datanode1
      - datanode2
    ports:
      - "8042:8042"
    networks:
      - hadoop_network

  datanode1:
    build: ./datanode
    container_name: datanode1
    depends_on:
      - namenode
    volumes:
      - hadoop_datanode1:/hadoop/dfs/data
    networks:
      - hadoop_network

  datanode2:
    build: ./datanode
    container_name: datanode2
    depends_on:
      - namenode
    volumes:
      - hadoop_datanode2:/hadoop/dfs/data
    networks:
      - hadoop_network

  datanode3:
    build: ./datanode
    container_name: datanode3
    depends_on:
      - namenode
    volumes:
      - hadoop_datanode3:/hadoop/dfs/data
    networks:
      - hadoop_network

volumes:
  hadoop_namenode:
  hadoop_datanode1:
  hadoop_datanode2:
  hadoop_datanode3:
  hadoop_historyserver:

networks:
  hadoop_network:
    name: hadoop_network
    external: true
```

4. Start the Hadoop Cluster
Run the script to create the network, build the Docker image, and start the Hadoop cluster.

```bash
#!/bin/bash

docker network create hadoop_network
docker build -t hadoop-base:3.3.6 .
docker-compose up -d
```

Save the script as start-cluster.sh and run it.

```bash
bash start-cluster.sh
```

## Accessing the Hadoop Cluster

NameNode Web UI: http://localhost:9870  
ResourceManager Web UI: http://localhost:8089  
HistoryServer Web UI: http://localhost:8188  
NodeManager Web UI: http://localhost:8042  

## Contributing
Feel free to submit issues and pull requests for improvements.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.
