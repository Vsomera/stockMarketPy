
# ACIT 3855 - Scalable API Microservices

A scalable python microservice application built with python and flask.


## Run Locally - with Docker

Clone the project

```bash
  git clone https://github.com/Vsomera/Python-Microservices.git
```

Go to the project directory

```bash
  cd ./Python-Microservices
```

Run application

```bash
  docker-compose up --build
```


Access mysql database - Locally Docker

```bash
  docker exec -it python-microservices-mysql_db-1 /bin/bash
```

Access AWS Ec2 Instance and containerized mySQL database

```bash
  ssh -i .\3855lab6.pem ubuntu@3.142.46.177
  docker exec  -it fc65ee95bebb /bin/bash
```

- Make sure to change create_tables_mysql.py drop_tables_mysql.py & app_conf.yml to switch from running locally and through the ec2 instance.

