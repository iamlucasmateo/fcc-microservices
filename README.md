# fcc-microservices
A simple microservices with message queueing architecture, run on Kubernetes 
- https://www.youtube.com/watch?v=hmkF77F9TLw


## Running ingress locally with minikube

- Map localhost (127.0.0.1) to mp3converter.com and rabbitmq-manager.com in /etc/hosts
- Enable ingress in minikube `minikube addons enable ingress`
- Run `minikube tunnel` to tunnel the ingress (i.e., similar to `kubectl port-forward <pod-name> 5000:5000`)


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

To connect to the MySQL Docker container running on Kubernetes from your local for debugging:
- `kubectl port-forward svc/mysql 3307:3306` (using the 3307 local port to avoid clashing with a local MySQL server)

## Connect to the MongoDB container

- To port forward the container: `kubectl port-forward svc/mongodb 27018:27017`
- To connect locally: `mongo mongodb://username:password@127.0.0.1:27018`
- Use database: `use <database>`
- Create user: 
```
use admin
db.createUser(
  {
    user: "fcc_micro_user",
    pwd: "fcc_micro_password",
    roles: [
      { role: "readWrite", db: "videos" }
    ]
  }
)
```

## Some cURL commands

- Login: `curl -X POST http://mp3converter.com/login -u <user>:<password>`
- POST a new video: `curl -X POST 'file=@./<full-path-to-file>' -H Authorization: Bearer <token> http://mp3converter.com/upload`