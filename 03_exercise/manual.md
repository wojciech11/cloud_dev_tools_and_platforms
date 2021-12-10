#  Azure EKS & Autoscale

## Stacja robocza

1. Rekomendowany: Linux (Ubuntu) / MacOS
2. Zainstalowane:

   - azure-cli ([instalacja](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
   - terraform ([instalacja](https://learn.hashicorp.com/tutorials/terraform/install-cli))
   - docker ([Ubuntu](#instalacja-docker-ubuntu), [MacOs, Windows](https://docs.docker.com/desktop/mac/install/))
   - Kubernetes CLI - [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/)
   - k3s - github.com/k3s-io/k3s
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

## Dodatkowe

- [Materiały szkolenie k8s](https://github.com/wojciech12/workshop_kubernetes_and_cloudnative/)
- [Co każdy programista powinien wiedzieć budując serwis dla Kubernetesa?](https://github.com/wojciech12/talk_k8s_what_should_every_dev_know)
- [Monitoring first, przykłady monitoringu dla Go, Py, Java](https://github.com/wojciech12/talk_monitoring_with_prometheus)
- [Zero-downtime deployments (dotnet core, Golang)](https://github.com/wojciech12/talk_zero_downtime_deployment_with_kubernetes)
