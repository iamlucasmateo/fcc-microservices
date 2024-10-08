# fcc-microservices
A simple microservices with message queueing architecture, run on Kubernetes 
- https://www.youtube.com/watch?v=hmkF77F9TLw


## Running ingress locally with minikube

- Map localhost (127.0.0.1) to mp3converter.com and rabbitmq-manager.com in /etc/hosts
- Enable ingress in minikube `minikube addons enable ingress`
- Run `minikube tunnel` to tunnel the ingress (i.e., similart to `kubectl port-forward <pod-name> 5000:5000`)


## Rabbit MQ

The RabbitMQ Broker is run as a StatefulSet with a PersistedVolumeClaim in Kubernetes so that messages are not lost if containers go down. 
Username and password for the RabbitMQ Manager console is `guest`


## Connect to the MySQL server from the MySQL client

-  `kubectl exec -it <mysql-client-pod> -- mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p<password>`
- `CREATE USER 'fcc'@'%' IDENTIFIED BY 'Admin_fcc123';`
- `GRANT ALL PRIVILEGES ON *.* TO 'fcc'@'%'`;
- `FLUSH PRIVILEGES;`
- `CREATE DATABASE <database-name>;`
- `CREATE TABLE users (email VARCHAR(255) PRIMARY KEY, password VARCHAR(255), isAdmin BOOL);`
- `INSERT INTO users (email, password, isAdmin) VALUES ('admin@fcc.org', '1234', true)`

## Some cURL commands

- Login: `curl -X POST http://mp3converter.com/login -u <user>:<password>`
- POST a new video: `curl -X POST 'file=@./<file-name>' -H Authorization: Bearer <token> http://mp3converter.com/upload`