FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y install python3.10
RUN apt-get -y install python3-pip

ENV AIRFLOW_HOME="/airflow"
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

RUN python3 -m pip install apache-airflow
RUN mkdir airflow


COPY initialize.sh .
RUN bash initialize.sh

ENV TZ=UTC