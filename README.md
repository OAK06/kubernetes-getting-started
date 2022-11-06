# Disclaimer

This is by no means a professional guide. I wrote this to summarize my very very basic understanding of docker and kubernetes, this guide is meant to provide the baby steps to just get started from not knowing what kubernetes is to deploying a Hello World page.

All non-hateful comments are welcome, I would love to have comments correcting any wrong info I've written.


# Getting Started: Docker / Kubernates


## Docker

The basic idea of docker is creating a virtual environment that runs the project, the virtual environment
should contain everything the project needs ex: configurations, dependencies, etc...

Steps:
- Install Docker
- Create a Dockerfile in the root of the project
- Create an image from the project
    - When building the image you need to set a tag to identify it.
    - PS: Don't ignore the dot at the end of the command, the dot refers to the current folder.
    - Command: `docker build -t '<name:version>' .`
- Push the image to a public/private registry
    - The registry is a place that stores your docker containers.
    - There are many services that provide this including docker themselves, I personally use Github's ghcr.io
    - It's important to set a specific tag when pushing to ghcr.io
        - Command: `docker build -t 'ghcr.io/<username>/<name:version>' .`
        - The tag in this case is the whole string 'ghcr.io/user/project:version'
    - To push to ghcr.io, you need to login your docker to ghcr.io
        - Command: `echo '<Github personal access token with registry permission>' | docker login ghcr.io -u <username> --password-stdin`
    - Once logged in you can push the image
        - Command: `docker image push <tag>`
    - You will find your image under the packages tab on github.

Now you have a container image in a registry and you can proceed to Kubernetes.


## Kubernetes

The basic idea for kubernetes is giving the user the ability to deal with servers in an abstract manner.
You don't need to manually install the project on every server you have.
You don't need to deal with server details and network structure between your servers.
Kubernetes is a big box where you can put all your toys.
Using a few configuration files kubernetes will manage your projects on its own.
You don't need to worry about which project files go on which server, it's all handled abstractly.

Kubernetes is an online service provided by hosting sites such as DigitalOcean, AWS, Google Cloud.
You'll need to create an account and start a Kubernetes cluster before doing anything (Costs money on a monthly basis).
The following steps are for DigitalOcean's Kubernetes environment.

Steps:
- Through DigitalOcean's control panel create a Kubernetes Cluster.
- To access the cluster you need to create a personal access token: `https://cloud.digitalocean.com/account/api/tokens`
- Install Kubectl & Doctl, these are command line tools used to access your Kubernetes environment.
- Now through your computer's local terminal you need to login using Doctl with your access token.
    - Command: `doctl auth init`
- Your Kubernetes cluster will need access to your ghcr registry when pulling the image
    - You can create a secret in your cluster that hold's its your github access token's value using kubectl
    - Command: `kubectl create secret docker-registry <label> --docker-server=https://ghcr.io --docker-username=<username> --docker-password=<github personal access token> --docker-email=<github email>`
- Now you can proceed to deploy your image either manually using commands or using .yaml files (.yaml is easier)
    - Example (You don't need to name the files like the following):
        - `deployment.yaml` (Configuration for the containers)
        - `service.yaml` (Configuration for the provided service enabling access to your containers, ex: http access)
        - You can execute these yaml files using kubectl:
            - Command `kubectl apply -f <filname with extension>`
        - To access your project through a public IP you need to expose the kubernetes internal port to the external port
            - Command `kubectl expose deployments <deployment-name> --type=LoadBalancer --port=<external-port> --target-port=<internal-port>`
        - You can run this command to find your external IP: `doctl compute load-balancer list --format Name,Created,IP,Status`
        - Or you can find the IP through the Kubernetes Dashboard on DigitalOcean
    - In this repo you'll find .yaml files for a stateful set, the stateful set creates pods that are stateful.
        - This means that regardless of what Kubernetes does to your pod, it will always come back using the same name, it also uses a number increment instead of a random string in the name. 
        - Ex: pod-01, pod-02, pod-03
