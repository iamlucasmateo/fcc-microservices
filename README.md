# fcc-microservices
A simple microservices with message queueing architecture, run on Kubernetes 
- https://www.youtube.com/watch?v=hmkF77F9TLw


## Running ingress locally with minikube

- Map localhost (127.0.0.1) to mp3converter.com
- Enable ingress in minikube `minikube addons enable ingress`
- Run `minikube tunnel` to tunnel the ingress (i.e., similart to `kubectl port-forward <pod-name> 5000:5000`)