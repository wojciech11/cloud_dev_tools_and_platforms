# Azure Key Vault i Azure Databases (WIP)

## Stacja robocza

1. Rekomendowany: Linux (Ubuntu) / MacOS
2. Zainstalowane:

   - azure-cli ([instalacja](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
   - terraform ([instalacja](https://learn.hashicorp.com/tutorials/terraform/install-cli))

## Azure Key Vault

Proszę przejdź do tutoriala w dokumentacji Azure: [Azure Kye Vault wiht a virtal machine](https://docs.microsoft.com/en-us/azure/key-vault/general/tutorial-python-virtual-machine?tabs=azure-cli).

## OAuth-aware proxy

Omówimy z prowadzącym: [Azure Proxy](https://docs.microsoft.com/en-us/azure/active-directory/app-proxy/application-proxy)

<img src="https://docs.microsoft.com/en-us/azure/active-directory/app-proxy/media/application-proxy/azureappproxxy.png" width="50%" />

Alternatywy, pozwalające również zabezpieczyć dostęp do wirtualnych maszyn:

- GCP: [IAP](https://cloud.google.com/iap); 
- AWS: [ALB+Cognito](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html) i [AWS SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html)

## Azure SQL Database for Postgres (WIP)

[Tutorial](https://docs.microsoft.com/en-us/azure/postgresql/quickstart-create-server-database-azure-cli)

<!-- ## Azure CosmosDB (WIP) -->

## Azure Cache for Redis

[Tutorial](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-python-get-started)

## Azure AD

TODO: Move to the slides.

Alternative: Okta, Auth0, and JumpCloud

## Dodatkowe

- [Types of Databases on Azure](https://azure.microsoft.com/en-us/product-categories/databases/)
