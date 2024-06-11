#!/bin/bash

docker network create hadoop_network

docker build -t hadoop-base:3.3.6 .

docker-compose up -d