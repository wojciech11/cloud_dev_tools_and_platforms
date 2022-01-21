# Azure AKS & Autoscale

## Stacja robocza

1. Rekomendowany: Linux (Ubuntu) / MacOS
2. Zainstalowane:

   - azure-cli ([instalacja](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
   - terraform ([instalacja](https://learn.hashicorp.com/tutorials/terraform/install-cli))
   - docker ([Ubuntu](#instalacja-docker-ubuntu), [MacOs, Windows](https://docs.docker.com/desktop/mac/install/))
   - Kubernetes CLI - [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/)
   - k3d - https://k3d.io/
   - helm - [helm.sh/docs/intro/install](https://helm.sh/docs/intro/install/)

3. Konto na [hub.docker.com](https://hub.docker.com/)

## Instalacja Docker Ubuntu

```bash
# install docker
sudo su

apt-get update ;
apt-get install -qq apt-transport-https ca-certificates curl software-properties-common ;
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - ;
add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu '$(lsb_release -cs)' stable' ;
apt-get update ;
apt-get install -qq docker-ce ;

# do not forget to exit
exit
```

## Docker

Co to jest Docker? Jak pracujemy z Dockerem?

```bash
docker ps
docker ps -a
docker images
```

```bash
# przykład
docker run --name wsb-cloud-dev \
    -e MYSQL_ROOT_PASSWORD=nomoresecrets \
    -d mysql

docker stop wsb-cloud-dev
```

Więcej o dobrych praktykach na [githubie](https://github.com/wojciech12/workshop_kubernetes_and_cloudnative/blob/master/00_docker/README.md).

## Azure Kubernetes Service (AKS)

Na podstawie [dokumentacji Azure](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough) ([terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster)), zobaczmy jak możemy utworzyć klaster AKSa i uruchomić przykładową aplikację.

### Utworzenie klastra

```bash
az login --use-device-code
```

```bash
export AKS_RESOURCE_GROUP=wsb-cloud-aks
az group create --name ${AKS_RESOURCE_GROUP} \
    --location eastus
```

```bash
az aks create --resource-group ${AKS_RESOURCE_GROUP} \
    --name myAKSCluster \
    --node-count 1 \
    --generate-ssh-keys
```

### Połączenie

```bash
# opcjonalne 
# jesli nie masz zainstalowanego kubectl
az aks install-cli
```

```bash
az aks get-credentials \
   --resource-group ${AKS_RESOURCE_GROUP} \
   --name myAKSCluster
```

```bash
# zobaczmy ile wezlow mamy
# w naszym klastrze
kubectl get nodes

 NAME                                STATUS   ROLES   AGE     VERSION
 aks-nodepool1-10484340-vmss000000   Ready    agent   2m11s   v1.21.7

kubectl get nodes -o wide
```

### Uruchomienie aplikacji

Wykorzystajmy [manifesty](https://github.com/wojciech12/workshop_kubernetes_and_cloudnative/tree/master/01_introduction/manifests), [aplikacji](https://github.com/wojciech12/workshop_kubernetes_and_cloudnative/tree/master/01_introduction/manifests/dockers) która wyświetla prostą stronę internetową.

```bash
git clone https://github.com/wojciech12/workshop_kubernetes_and_cloudnative.git
```

```bash
cd workshop_kubernetes_and_cloudnative/01_introduction

kubectl apply -f manifests/kube-deployment.yaml

kubectl apply -f manifests/kube-service.yaml
```

```bash
kubectl get pods

kubectl get deploy

kubectl get svc
```

```bash
curl PUBLIC_IP:8080

<html>
<h1>1.0.0</h1>
</html>
```

```bash
# skalowanie
kubectl scale deployment/intro-app-deploy --replicas=2

kubectl get pods
```

### Zakończenie pracy

```bash
az group delete --name ${AKS_RESOURCE_GROUP}
```

## Kubernetes z k3s

### Przygotowanie do pracy

Za [instrukcją ćwiczeń z Kubernetesa](https://github.com/wojciech12/workshop_kubernetes_and_cloudnative/blob/master/01_introduction/introduction.pdf), przygotujmy lokalne środowisko do pracy:

```bash
k3d cluster create --port "8080:8080@loadbalancer" \
                   --port "8000:80@loadbalancer" \
                   'k8s-w10i-workshop'
```

```bash
kubectl config use-context k3d-k8s-w10i-workshop
kubectl cluster-info

Kubernetes control plane is running at https://0.0.0.0:60602
CoreDNS is running at https://...
Metrics-server is running at https://...
```

### Ćwiczenia

Przejdź do [instrukcji](https://github.com/wojciech12/workshop_kubernetes_and_cloudnative/blob/master/01_introduction/introduction.pdf).

## Azure containers

Azure containers są odpowiednikiem AWS Fargate dla Azure. Proszę wykonać kroki opisane w [dokumentacji Azure](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-quickstart).

## Dodatkowe

- [Ekosystem projektów CloudNative](https://landscape.cncf.io/)
- Jeśli budujemy Continuous Deployment:
  - [argocd](https://argo-cd.readthedocs.io/en/stable/)
  - [spinnaker](https://spinnaker.io/)
  - [gitlab](https://about.gitlab.com/) lub [github](https://github.com)
- [Co każdy programista powinien wiedzieć budując serwis dla Kubernetesa?](https://github.com/wojciech12/talk_k8s_what_should_every_dev_know)
- [Monitoring first, przykłady monitoringu dla Go, Py, Java](https://github.com/wojciech12/talk_monitoring_with_prometheus)
- [Zero-downtime deployments (dotnet core, Golang)](https://github.com/wojciech12/talk_zero_downtime_deployment_with_kubernetes)
