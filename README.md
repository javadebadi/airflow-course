<h1 style="align-items: center; text-align: center">
    Workflow Management using Airflow in Python  <img src="https://upload.wikimedia.org/wikipedia/commons/d/de/AirflowLogo.png" width="100">
</h1>
# Workflow Management with Airflow in Python

## Installation
Airflow is written in Python and therefore you need to install Python in your OS or docker container. Since the goal of this tutorial is to teach how to use airflow, we will start with simplest setup and continue to add further tools later.

### Installation on Linux
If Python is not installed on your Linux OS, install it. We will use Python 3.10 and recommend that you use the same version too.
First create a virtual environment:
```bash
python3 -m venv. venv
```
Next, activate the virtual environment
```bash
source .venv/bin/activate
```
Then, run the following command to install Apache Airflow:
```bash
python3 -m pip install apache-airflow
```
After installion is finished you must have a directory in this address: `~/ariflow` with following subdirectories:
- `dags`
- `plugins`
- `logs`
Airflow needs a database. The default database is an Sqlite and for simplicity we will go with default for now. To initialize the database, we run the following command:
```bash
airflow db init
```
Afther the database is initialized, we can create a user with admin permission for login to airflow webserver:

```bash
airflow users create --username admin\
                     --password admin\
                     --firstname Javad\
                     --lastname Ebadi\
                     --role Admin\
                     --email javad.ebadi.1990@gmail.com

```



### Installation on Windows

In Windows OS, installation of Airflow is tricky. The simplest solution to install Airflow on a Windows OS is to use Docker.

In order to use this method, you have to install Docker and docker-compose in your machine. [Here](https://docs.docker.com/desktop/install/windows-install/) is the information to know how to install Docker on you Windows machine.

In your local computer, create a directoy and name it `airflow`.  For example, you can use git-bash as follows:

```bash
mkdir ~/airflow
```

Navigate insdie the local `airflow` directoy and copy all of the files inside `https://github.com/javadebadi/airflow-course/installation/simple/` to your local `airflow` directory.

Next, make sure docker engine is up and running your machine, then open a powershell windows inside `airflow` directory and execute the following command:

```bash
docker-compose up
```

To test that you have installed it successfully, open this link in browser: [http://localhost:8080](http://localhost:8080)