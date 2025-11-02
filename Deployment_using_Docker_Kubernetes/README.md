# IoT-Based Room Temperature Controller  
<!--
## Table of Contents
- [Project Structure](#project-structure)
    - [1.1 Project Sub-structure](#project-sub-structure)

A simple **Flask-based microservice** running inside **Docker** and deployed on **K3s (lightweight Kubernetes)**.
It provides API endpoints to view and modify a target room temperature, and integrates easily with a history data service.

---

## Project Structure
### Project Sub-structure





---

## Prerequisites
|   |   |
|---|---|
| **Docker** | For building and running containers locally | 
| **K3s** | Lightweight Kubernetes distribution |
| **kubectl** | CLI tool for managing Kubernetes resources |
| **curl** | To test endpoints | 

---

### Step 1: Build the Docker Image
Navigate to your `Server/` directory and build:

```bash
docker build -t my-server-app:v1_01 .
```

!-->

## Docker Command Summary
|Purpose |Command|Description|
|---|---|---|
|Build an image | `docker build -t myapp:v1 .` | Build image from Dockerfile in current directory.|
|List images|`docker images`|Show all local Docker images.|
|Run a container|`docker run -p 5000:5000 myapp:v1`|Start a container and map port 5000.|
|List running containers|`docker ps`|Show running containers.|
|List all containers (even stopped)|`docker ps -a`|Show all containers.|
|Stop a container|`docker stop <container_id>`|Gracefully stop container.|
|Remove a container|`docker rm <container_id>`|Delete stopped container.|
|Remove an image|`docker rmi myapp:v1`|Delete image from local cache.|
|Tag an image|`docker tag myapp:v1_01 myapp:v2_01`|Create new tag/version.
|Save image to tar|`docker save myapp:v1 > myapp_v1.tar`|Export image as tar archive.|
|Load image from tar| `docker load < myapp_v1.tar`|Import saved image.|
|Push image to registry|`docker push myrepo/myapp:v1`|Upload to Docker registry.|
|Run local registry|`docker run -d -p 5000:5000 --name registry registry:2`|Start local Docker registry.|
|Push to local registry|`docker tag myapp:v1 localhost:5000/myapp:v1 && docker push localhost:5000/myapp:v1`|Push image to local registry.|

---

## Docker Network

|Purpose|Command|Description|
|---|---|---|
|Create a Docker Network|`docker network create iot_network`|Create a docker network `iot_network`|
|Run `Server` app|`docker run -d --name server --network iot_network -p 5000:5000 server_image:v1_01`|Run the docker image `server_image:v1_01`|
|Run `Data Service` app|`docker run -d --name data_service --network iot_network -p 5001:5001 data_service_image:v1_01`|Run the docker image `data_service_image:v1_01`|

---


## Kubernetes / K3s Command Summary
### Deploy and Manage Applications
|Purpose|Command|Description|
|---|---|---|
|Apply configuration|`kubectl apply -f deployment.yaml`|Create or update a deployment.|
|Apply service|`kubectl apply -f service.yaml`|Create or update a service.|
|View resources|`kubectl get all`|Show pods, services, deployments, etc.|
|View deployments|`kubectl get deployments`|List deployments.|
|View pods|`kubectl get pods`|List pods.|
|View services|`kubectl get svc`|List services.|
|View ingress|`kubectl get ingress`|List ingress resources.|
|View logs|`kubectl logs <pod_name>`|Show logs of a running pod.|
|Describe pod/deployment|`kubectl describe pod <pod_name>`|Show detailed status and events.|

---

### Scaling, Deleting, and Updating
|Purpose|Command|Description|
|---|---|---|
|Scale deployment|`kubectl scale deployment myapp --replicas=3`|Run 3 pods.|
|Stop deployment (0 pods)|`kubectl scale deployment myapp --replicas=0`|Stop all pods.|
|Delete deployment|`kubectl delete deployment myapp`|Remove deployment and pods.|
|Delete service|`kubectl delete svc myapp-service`|Remove service.|
|Delete all resources|`kubectl delete all --all`|Clean up entire namespace.|
|Edit deployment live|`kubectl edit deployment myapp`|Open YAML in editor.|

---

### Debugging and Access
|Purpose|Command|Description|
|---|---|---|
|Check pod logs|`kubectl logs <pod_name>`|View logs inside a container.|
|Execute shell in pod|`kubectl exec -it <pod_name> -- /bin/bash`|Access container shell.|
|Port forwarding|`kubectl port-forward svc/myapp-service 5000:80`|Access app locally via 127.0.0.1:5000.|
|Get cluster info|`kubectl cluster-info`|Show K3s/Kubernetes control plane endpoints.|
|List namespaces|`kubectl get ns`|List all namespaces.|

---

### Image Management (K3s Specific)
|Purpose|Command|Description|
|---|---|---|
|Import local Docker image into K3s|`docker save myapp:v1 \| sudo k3s ctr images import -`| Import image to K3s|
|List images in K3s|`sudo k3s ctr images list`|View containerd images in K3s.|
|Remove image from K3s|`sudo k3s ctr images rm <image_name>`|Delete image from containerd store.|

---

### Ingress & External Access
|Purpose|Command|Description|
|---|---|---|
|Create ingress|`kubectl apply -f ingress.yaml`|Deploy ingress rules.|
|View ingress|`kubectl get ingress`|List ingress resources.|
|Describe ingress|`kubectl describe ingress myapp-ingress`|See host/path rules.|

---

