# Pierwsze spotkanie

## Stacja robocza

1. Rekomendowany: Linux (Ubuntu) / MacOS
2. Zainstalowane:

   - azure-cli ([instalacje](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
   - terraform
   - pulumi

## Założenie konta

1. Zaloguj się na https://portal.azure.com posługując się loginem i hasłem wsb.

2. Wybierz *Access student benefits*, naciskając *Explore*

3. Podając dane, podaj dane [WSB](https://www.google.com/search?q=wsb+maps+wroclaw).

4. Na portal.azure.com, w prawym górnym roku będziesz miał rozwijane menu, otwórz *Cost Management + Biling*

## Uwagi 

Pamiętajcie proszę o usunięciu resource groupy, w której utworzyliście wasze zasoby, po zajęciach.

## Utworzenie Wirtualnej Maszyny

### Wymagania

Rozmiar VM:

| Parametr     | Wartość                     |
| ------------ | --------------------------- |
| VM size      | General Purpose 4GiB  (B2s) |
| OS           | Ubuntu  20.04LTS            |
| Inbound port | 22, 80                      |
| Region       | eastus                      |

Jak się będziemy logować?

| Parametr            | Wartość                               |
| ------------------  | ------------------------------------- |
| Authentication Type | Password* (nie rób tego w produkcji!) |
| Username            | ubuntu                                |

### Web Portal (1)

Utworzenie VM przez interfejs webowy:

1. Wybierz *Virtual machines* w menu portalu Azure.

2. Teraz *+Create*.

3. Wypełnij pola według wymagań, utwórz *Resource Group* - wsb

4. Wybierz *Review and Create*.

Weryfikacja czy maszyna działa:

1. Wyszukaj *Public IP address**, będziemy go potrzebować do zalogowania się do VM.

2. Zaloguj się posługując się *ssh* lub *putty*:

   ```bash

   ssh ubuntu@40.X.X.X

   ubuntu@wsb:~$ ls

   ubuntu@wsb:~$ lsb_release  -a

   No LSB modules are available.
   Distributor ID:	Ubuntu
   Description:	Ubuntu 20.04.3 LTS
   Release:	20.04
   Codename:	focal
   ```

3. Zainstaluj nginx, aby zweryfikować czy możemy się połączyć do maszyny na porcie 80.

   ```bash
   ubuntu@wsb:~$ sudo apt-get update;

   ubuntu@wsb:~$ sudo apt-get install -y nginx

   # sprawdzmy czy nginx nasluchuje
   # lokalnie
   ubuntu@wsb:~$ curl 127.0.0.1:80
   ```

4. Na swoim komputerze, w przeglądarce lub w konsoli:

   ```bash
   curl 40.X.X.X
   ```

5. Może jednak tak nie jest... zmieńmy domyślną stronę wyświetl przez nginxa:

    ```bash
    sudo nano /var/www/html/index.nginx-debian.html
    ```

    Zapisz, sprawdź lokalnie, a potem ze swojego komputera.

Informacje o VM:

1. Przeglądnij parametry wirtualnej maszyny.
2. Zanotuj:

   - jak duży dysk nasza VM ma
   - Jaki był najwyższe zużycie procesora?

Konsola w przeglądarce *[>_]*:

1. Wybierz *[>_]* i uruchom bash.

2. Zaloguj się do swojej maszyny.

3. Sprawdź czy *git* jest zainstalowany.

Zatrzymywanie:

1. Zatrzymaj maszynę VM.

   Zauważ nie płacisz za uruchomioną maszynę, tylko za statyczne zasoby, np., przestrzeń dyskową.

2. Uruchom ponownie i zaloguj się przez ssh.

   Co się zmieniło?

Kasowanie:

- Skasuj swoją wirtualną maszynę :fire:

### Azure CLI

Nie powinno się używać interfejsu webowego do tworzenia zasobów, minimalna akceptowalna forma to script z komendami `az` lub plik README.

*Zauważ to ćwiczenie możemy tez zrobić w konsoli bash w portalu.*

1. Logowanie

   ```bash
   # automatycznie otworzy przegląndarkę
   az login

   # wyświetli URL i kod do przeklejenia
   az login --use-device-code
   ```

2. Sprawdźmy czy wszystko działa.

   ```bash
   az  account list
   ```

   Powinnaś / powinieneś zobaczyć informacje o swoim koncie.

3. Utwórz resource group w regionie `eastus`.

4. Sprawdźmy jakie grupy zasobów mamy:

   ```bash
   az group list

   az group list --query '[].name'

   az group list --query '[].[name,location]' -o tsv
   ```

   Podpowiedź: warto mieć zainstalowane `jq` ([download](https://stedolan.github.io/jq/download/)).

5. Utwórzmy teraz VM za pomocą azure-cli.

   Komenda:

   ```bash
   az vm create \
     --location <region> \
     --resource-group <nazwa-grupy-zasobów> \
     --name <nazwa-maszyny> \
     --size <rozmiar-maszyny> \
     --image <obraz-systemu> \
     --public-ip-sku Standard \
     --admin-username <nazwa-użytkownika> \
     --admin-password <haslo>
   ```

   Pamiętaj:

   Poza ćwiczeniami nigdy nie wybieraj logowania się przez użytkownika i hasło, zawsze wybieraj logowanie się za pomocą kluczy ssh, na przykład za pomocą opcji `--generate-ssh-keys`.

   Problem. Region mamy. Co mam wpisać pod inne wartości :/

6. Jak znaleźć X?

   VM size:

   ```bash
   #
   az vm list-sizes \
     --location eastus \
     --output table

   # znajdź B1s
   az vm list-sizes \
     --location eastus \
     --output table | head
   ```

   Image:

   ```bash
   az vm image list \
   --location eastus \
   --output table
   ```

   ```bash
   # możemy wyszukiwać po polach
   az vm image list \
     --offer ubuntu \
     --publisher Canonical \
     --sku "20_04-lts" \
     --location eastus \
     --all
   ```
7. Na podstawie zdobytych informacji, utwórz wirtualną maszynę:

   ```bash
   az vm create...
   ```

8. Zweryfikuj czy widzisz VM w portalu.

   ```bash
   az vm list --output table
   ```

9. Zaloguj się na VM. Zainstaluj nginxa oraz otwórz port 80, korzystając z komendy open-port opisanej w [dokumentacji](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/nsg-quickstart#quickly-open-a-port-for-a-vm). Zweryfikuj czy możesz się połączyć z ngixem.

10. Skasuj wszystkie zasoby:

    ```bash
    # zastąp myResourceGroup twoją nazwą grupy zasobów
    az group delete --name myResourceGroup
    ```

### Terraform

State-of-the-art. Obecnie Terraform i Terragrunt uznawane za najlepsze narzędzie dla Infrastructure-as-a-Code.

1. Zainstaluj terraform na twoim komputerze według [instrukcji](https://learn.hashicorp.com/tutorials/terraform/install-cli).

2. Korzystając z dokumentacji [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
) i [przykładów](https://github.com/hashicorp/terraform-provider-azurerm/tree/main/examples/virtual-machines), utwórzmy w następnych krokach maszynę wirtualną.

3. Przygotuj projekt.

   ```bash
   mkdir azure-tf
   cd azure-tf
   touch main.tf
   ```

4. Do `main.tf` przekopiuj definicję providera ([na podstawie przykładu](https://github.com/hashicorp/terraform-provider-azurerm/tree/main/examples/virtual-machines/linux/basic-password)):

   ```terraform
   provider "azurerm" {
     features {}
   }
   ```

   Zanim, pójdziemy dalej zainicjujmy projekt:

   ```bash
   terraform init
   ```

5. Do `main.tf` przekopuj kilka zasobów i uruchom `terraform plan`,

   ```terraform
   provider "azurerm" {
     features {}
   }

   variable "password" {
     description = "The password for the VM to login over ssh"
   }

   resource "azurerm_resource_group" "main" {
     name     = "wsb-resources"
     location = "eastus"
   }

   resource "azurerm_virtual_network" "main" {
     name                = "wsb-network"
     address_space       = ["10.0.0.0/22"]
     location            = azurerm_resource_group.main.location
     resource_group_name = azurerm_resource_group.main.name
   }

   resource "azurerm_subnet" "internal" {
     name                 = "internal"
     resource_group_name  = azurerm_resource_group.main.name
     virtual_network_name = azurerm_virtual_network.main.name
     address_prefixes     = ["10.0.2.0/24"]
   }

   resource "azurerm_public_ip" "public_ip" {
     name                = "wsb-public-ip"
     resource_group_name = azurerm_resource_group.main.name
     location            = azurerm_resource_group.main.location
     allocation_method   = "Dynamic"
   }

   resource "azurerm_network_interface" "main" {
     name                = "wsb-nic"
     resource_group_name = azurerm_resource_group.main.name
     location            = azurerm_resource_group.main.location

     ip_configuration {
       name                          = "internal"
       subnet_id                     = azurerm_subnet.internal.id
       private_ip_address_allocation = "Dynamic"

       public_ip_address_id = azurerm_public_ip.public_ip.id
     }
   }

   resource "azurerm_linux_virtual_machine" "main" {
     name                            = "wsb-vm"
     resource_group_name             = azurerm_resource_group.main.name
     location                        = azurerm_resource_group.main.location
     size                            = "Standard_B1ls"
     admin_username                  = "ubuntu"
     admin_password                  = var.password
     disable_password_authentication = false
     network_interface_ids = [
       azurerm_network_interface.main.id,
     ]

     source_image_reference {
       publisher = "Canonical"
       offer     = "UbuntuServer"
       sku       = "18.04-LTS"
       version   = "latest"
     }

     os_disk {
       storage_account_type = "Standard_LRS"
       caching              = "ReadWrite"
     }
   }
   ```

   Niezwykle pomocną komendą jest również `terraform fmt`.

5. Zobacz jakie pliki Terraform utworzył:

   ```bash
   ls
   ```

   Wyszukaj hasła w nowych plikach.

6. Zaloguj się do swojej maszyny:

   ```bash
   ssh ubuntu@X.Y.Z.V
   ```

6. Dodaj tagi ([azure](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources?tabs=json), [aws](https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html)) do swojej wirtualnej maszyny

7. Usuń tylko definicję maszyny wirtualnej z `main.tf` i wywołaj `terraform apply`.

8. Dodatkowe:

   - wyświetlij IP address z pomocą [outputs](https://www.terraform.io/docs/language/values/outputs.html)
   - generacja hasła z [password resource](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password)

9. Usuńmy wszystko:

   ```bash
   terraform destroy
   ```

Zauważ: Moglibyśmy również zainstalować wymagane pakiety z poziomu Terraforma posługując się *Provisioner*, na przykład, [remote-exec](https://www.terraform.io/docs/language/resources/provisioners/remote-exec.html). Więcej informacji znajdziesz w [dokumentacji](https://www.terraform.io/docs/language/resources/provisioners/syntax.html).

### Pulumi (dodatkowe)

*New kid on the block*. Pozwala łączyć kod konfigurujący maszynę (na przykład co zainstalować) z deklaracją infrastruktury. Wszystko za pomocą języka programowania znanego programistom.

1. Zainstaluj Pulumi korzystając z [instrukcji](https://www.pulumi.com/docs/get-started/install/)

2. Przygotujmy pierwszy projekt:

   ```bash
   mkdir azure-pulumi && cd azure-pulumi

   # jeśli nie chcesz korzystać 
   # z chmury pulumi
   #
   # pulumi login --local

   pulumi new azure-python
   ```

3. Przeglądnij `__main__.py`, zmieć nazwę grupy zasobów i nazwy konta dla storage, następnie uruchom pulumi:

   ```bash
   pulumi up
   ```

5. Zobacz czy w konsoli został utworzony storage w konsoli web.

6. Skasuj:

   ```bash
   pulumi destroy
   ```

7. Jak utworzyć VM, można zobaczyć w [tutorialu](https://dev-clone.nuxtjs.app/pulumidev/786495).

### Inne narzędzia

Infrastruktura:

- Są też Azure RM templates, podobne do AWS CloudFormation

Deployment/configuration mgmt:

- Ansible
- Saltstack
- AWS: [AWS CDK](https://aws.amazon.com/cdk/)

Platformy do pracy w zespole nad infrastrukturze:

- [spacelift.io](https://spacelift.io/)

<!--
## Materiały dodatkowe
-->
<!--
- [Quick create VM in portal](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-portal)
-->
<!--
az vm create \
  --resource-group wsb_group \
  --name moja-vm-2 \
  --size Standard_B1ls \
  --image "Canonical:0001-com-ubuntu-server-focal:20_04-lts-gen2:latest" \
  --admin-username ubuntu \
  --admin-password mojehaslo

az group delete --name wsb_group
-->
