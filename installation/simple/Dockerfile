FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y install python3.10
RUN apt-get -y install python3-pip
RUN python3 -m pip install apache-airflow

COPY initialize.sh .
RUN bash initialize.sh

ENV TZ=UTC