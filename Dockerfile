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