# API_Doccker_Kubernestes_Projet2
This work is about to predict the nature of banking transactions on a dataset with an initial size of (151112, 10). 
The nature of a transaction can have two states, fraudulent (1) and non-fraudulent (0).

Two algorithms were used. KNeighborsClassifier and CatBoostClassifier.

Below instructions below will be used for:
- The creation of API docker image of both prediction models
- The creation of API tests docker images
- The creation of these images containers
- The creation of a Kubernetes API deployment. This deployment contains on 3 pods



Installation and usage:

Note: the dot at line command creating images does not indicate the end of a sentence, but the current folder.
Note2: The images can either be created locally and then pushed to Docker hub, or pulled directly from Docker hub with the appropriate name.


- Install the required packages listed in the requirements.txt file. Command: pip install requirments.txt

- Generate the two machine learning models. Command: python3 ml_pour_generer_model.py

- Create fraud_project_api image of the API. Command: docker build -f DockerFile -t ali07datascientest/fraud-project:fastapi.0.2 .

- Push the image into Docker hub. Command: docker push ali07datascientest/fraud-project

- Create functionnal_test_api image. It tests the proper functioning of the API. Command: docker image build -f Dockerfile_is_functionnal_test -t ali07datascientest/is-functional-test:0.2 .

- Push the image into Docker hub. Command: docker push ali07datascientest/is-functional-test:0.2

- Create fraud-project-tests image. It tests PUT curl of the API. Command: docker image build -f DockerFile_API_test -t ali07datascientest/fraud-project-tests:0.2 .

- Push the image into Docker hub. Command: docker push ali07datascientest/fraud-project-tests:0.2

- Start minikube. Command: minicub start

- Use this address to interact with the API

- After minikube is installed and started, minikube dashboard launched, execute this command to get dashboard IP address: kubectl proxy --address='0.0.0.0' --disable-filter=true  

- Run and deploy the API, with Kubernetes, by creating a service of 3 pods. Command: kubectl create -f my-deployment-eval.yml

- Create ClusterIp service. Commande: kubectl create -f my-service-eval.yml

- Enable ingress. Command : minikube addons enable ingress

- And then expose the service. Command: kubectl create -f my-ingress-eval.yml

- Execute this command to get IP address of the Ingress: kubectl get ingress


First connection to the API:
We can connect to the API only with these 3 credentials:

user1: Bachir, Password: bachir123
user2: Ali, Password: ali123
user3: API_Fraud, Password: apifraud123
