# Serverless i PaaS

## Stacja robocza

1. Rekomendowany: Linux (Ubuntu) / MacOS
2. Zainstalowane:

   - azure-cli ([instalacje](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
   - azure functions core tools ([instalacja](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local))
   - [httpie](https://httpie.io/cli) albo curl
   - AWS SAM ([instalacja](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html))
   - [serverless](https://www.serverless.com/) - poniżej instrukcja
   - terraform (opcjonalnie)

## Logowanie z użyciem kluczy ssh

Trochę powtórki z ostatnich zajęć, jak logujemy się za pomocą kluczy ssh.

1. Utwórz swój klucz ssh:

   ```bash
   ssh-keygen -f ~/.ssh/wsb_id_rsa -t rsa -b 4092
   ls ~/.ssh
   ```

2. Utwórz maszynę wirtualną dodając nasz klucz ssh (patrz ostatnie ćwiczenia [01_exercise](../01_exercise/manual.md)): 

   ```bash
   az vm create \
     --location <region> \
     --resource-group <nazwa-grupy-zasobów> \
     --name <nazwa-maszyny> \
     --size <rozmiar-maszyny> \
     --image <obraz-systemu> \
     --public-ip-sku Standard \
     --ssh-key-value ~/.ssh/wsb_id_rsa.pub
   ```

3. zaloguj się z uzyciem klucza ssh:

   ```bash
   ssh ubuntu@<IP_ADDRESS>

   # jak debugować?
   ssh ubuntu@<IP_ADDRESS>  -vvv

   # a teraz ze wskazaniem klucza,
   # który chcemy uzyc
   ssh ubuntu@<IP_ADDRESS> -i ~/.ssh/wsb_id_rsa
   ```

4. A co gdy mamy sporo maszyn i chcemy w różny sposób się do nich logujemy, tutaj z pomocą przychodzi nam `~/.ssh/config`:

   ```bash
   # code
   atom ~/.ssh/config
   ```

   ```
   Host <IP_ADDRESS>
     IdentityFile ~/.ssh/wsb_id_rsa
   ```

5. Jeszcze jedno, jak to mawiał... ssh agent. Zamiast specyfikować klucz lub wybierać konfigurację, możemy dodać klucz do agenda ssh:

   ```bash
   eval "$(ssh-agent -s)"

   ssh-add ~/.ssh/wsb_id_rsa

   ssh-add -L

   # teraz możemy się spokojnie zalogować
   ssh ubuntu@<IP_ADDRESS>
   ```

6. Dostarczyciele chmury oferują lepszą alternatywę do logowania się, na przykład dla AWS, [AWS EC2 Instance Connect](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Connect-using-EC2-Instance-Connect.html) lub, zdecydowanie bardziej bezpieczny, [AWS SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html).

7. Usuń maszynę wirtualną z której korzystaliśmy w tym ćwiczeniu.

## Serverless - Azure Functions

Upewnij się czy masz zainstalowane [Azure Function Core CLI](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local):

```bash
func --version
```

### Lokalnie

Ćwiczenie na podstawie [Your first Function in Py](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python):

1. Jak to na każdego dobrego dewelopera Python, zaczynamy od wirtualnego środowiska:

   ```bash
   python -m venv .venv
   ```

2. Utwórz twój pierwszy projekt:
   
   ```bash
   func init YourProjectName --python

   # na przyklad
   func init WsbHelloWorld --python
   ```

3. Zapoznaj się z plikami:

   ```bash
   ls
   # atom
   code YourProjectName
   ```

4. Utwórz pierwszy HTTP handler:

   ```bash
   cd YourProjectName
   func new --name HttpHelloMsg --template "HTTP trigger" --authlevel "anonymous"

   # powinienes zobaczyc nowy folder:
   ls

   ...
   HttpHelloMsg
   ...
   ```

5. Lokalne testowanie:

   ```bash
   func start

   # w osobnym oknie:
   curl 'http://localhost:7071/api/HttpHelloMsg?name=Natalia'
   ```

5. Zmodyfikuj zwracaną wiadomość i przetestuj, że działa.

### Publikowanie - zasoby podstawowe

1. Login:

   ```bash
   # lub po prostu az login
   az login --use-device-code

   # dosc pomocne
   az config param-persist on
   ```

2. Czas utworzyć zasoby:

   ```bash
   export AZ_RESOURCE_GROUP=<YOUR GROUP NAME FOR FUNCTION>

   az group create \
     --name ${AZ_RESOURCE_GROUP} \
     --location eastus

   # potrzebny dla umieszczenia naszego kodu
   # zauwaz STORAGE_NAME musi być unikalną globalnie nazwą
   export AZ_STORAGE_ACCOUNT=<storage name for function>

   az storage account create \
      --name ${AZ_STORAGE_ACCOUNT} \
      --sku Standard_LRS \
      --location eastus \
      --resource-group ${AZ_RESOURCE_GROUP}

   # zauwaz: APP_NAME musi być globalnie unikalną nazwą
   export AZ_FUNC_APP_NAME=<YOUR APP NAME>

   az functionapp create \
      --consumption-plan-location eastus \
      --runtime python \
      --runtime-version 3.8 \
      --functions-version 3 \
      --os-type linux \
      --resource-group ${AZ_RESOURCE_GROUP} \
      --storage-account ${AZ_STORAGE_ACCOUNT} \
      --name ${AZ_FUNC_APP_NAME}
   ```

   Więcej o Consumption Plans w [dokumentacji Azure](https://docs.microsoft.com/en-us/azure/azure-functions/consumption-plan).

3. Szybkie spojrzenie do portalu, przejdź do zakładki `Function App`.

Zauważ, mógłbyś utworzyć powyższe zasoby posługując się [terraformem](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/function_app).

<!-- https://itnext.io/introduction-to-azure-functions-using-terraform-eca009ddf437 -->

### Publikowanie Funkccji

Teraz czas, aby naszą funkcję opublikować:

```bash

func azure functionapp publish ${AZ_FUNC_APP_NAME}
```

i smoke test:

```bash

# jesli nie `httpie` to `curl` oczywiscie
http <INVOKE URL>
```

Możesz teraz usunąć aplikację:

```bash
az functionapp delete --name ${AZ_FUNC_APP_NAME}

az functionapp list
```

Jak wszystko działa to czas, wykasować:

```bash
az group delete --resource-group ${AZ_RESOURCE_GROUP}
```

### Node z Serverless

Najpopularniejszym frameworkiem/narzędziem pracy z serverless jest [serverless](https://github.com/serverless/serverless). Inspiracją dla ćwiczenia jest oficjalny [quickstart dla Azure](https://www.serverless.com/framework/docs/providers/azure/guide/quick-start).

1. Zainstaluj:

   - upewnij się, że masz node zainstalowany, w wersji wspieranej przez Azure-a ([dokumentacja](https://aka.ms/functions-node-versions)),
   - jeśli nie, zainstaluj node za pomocą [nvm](https://github.com/nvm-sh/nvm),
   - serverless według [instrukcji](https://www.serverless.com/framework/docs/getting-started).

2. Przejdź do katalogu w których chcesz utworzyć projekt.

3. Utwórz projekt:

   ```bash
   # wybierz swoją nazwę
   sls create -t azure-nodejs -p WsbHelloWorld

   npm install
   ```

4. Lokalnie:

   ```bash
   sls offline
   ``` 

5. `dry-run`, we like:

   ```bash
   sls deploy --dryrun

   # arn?
   sls deploy --dryrun --arn
   ```

6. Deployment:

   ```bash
   sls deploy
   sls info
   ````

7. Przetestuj czy możesz się połączyć za pomocą `curl` albo `http`.

8. Zapoznaj się jak możemy wywoływać naszą funkcję z użyciem `sls invoke` i `sls invoke local` korzystając z [tutoriala](https://www.serverless.com/framework/docs/providers/azure/guide/quick-start#test-your-function-app). 

8. Wykasuj nasz serwis:

   ```bash
   sls remove
   ``` 

Zauważ, serverless ma wsparcia dla [stage-ów](https://serverless.readme.io/docs/stage-create). Przykłady znajdziesz na [githubie](https://github.com/serverless/serverless-azure-functions/blob/master/docs/examples/).

## Serverless && AWS

Na AWSie publikujemy naszą aplikację zazwyczaj za AWS API Gateway, jeśli chodzi o obsługę ruchu http:

```
         --------       --------
User -> |   API   | -> |  AWS   |
        | Gateway |    | Lambda |
         ---------      --------

```

1. Z Serverless:

  ```bash
  # zobaczmy jakie mamy opcje
  serverless create -t aws

  # 
  serverless create -t aws-nodejs --path HelloWorldAWS

  cd HelloWorldAWS

  # tradycyjnie, najpierw sprawdzamy czy wszystko dziala
  sls invoke local -f hello 

  sls invoke local -f hello -d '{"name": "wojtek"}'
  ```

2. Z AWS SAM, pierwszy krok to oczywiście [instalacja narzędzia](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html):

  ```bash
  # wygenerujmy przykladowy serwis
  # wybierajac domyslne wartosci
  sam init

  # wywolanie lokalne lambdy (1)
  cd FOLDER_Z_TWOJA_APP
  sam local start-api

  curl http://127.0.0.1:3000/hello
  ```

  ```bash
  # wywolanie lokalnie lambdy (2)
  sam local invoke -e events/event.json

  # zauwaz, ze mozesz wygenerowac rozne eventy
  # dla testowania lambdy, ktora reaguje na eventy
  # z roznych serwisow AWSa
  sam local generate-event apigateway authorizer
  ```

## PaaS - Azure

Ćwiczenie zainspirowane [quickstart for Python](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python).

1. Przejdź do [py_hello_world](./py_hello_world). Znajdziesz tutaj prostą aplikację flask.

2. Uruchom ją według poleceń w pliku [README.md](./py_hello_world/README.md).

3. Utwórz dedykowaną grupę, a następnie uruchom naszą bardzo złożoną aplikację w chmurze:

   ```bash
   export AZ_RESOURCE_GROUP=<NAZWA DLA TWOJEJ GRUPY>

   # tu tworzenie twojej resource group

   # deploy aplikacji
   az webapp up --sku B1 \
     --resource-group ${AZ_RESOURCE_GROUP} \
     --name <app-name>

   az webapp list -o table
   ```

4. Przejdźmy do portalu, znajdźmy naszą aplikację (w *App Services*).

5. Testujemy, jak coś nie działa, sprawdź kod http odpowiedzi. Możesz również sprawdzić logi (komendę znajdziesz w [dokumentacji Azure](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)).

6. Zmień output serwisu, zrób deployment i przetestuj.

7. ... i kasujemy:

   ```bash
   az group delete --resource-group ${AZ_RESOURCE_GROUP}
   ```

## PaaS - Heroku 

Zobaczmy jak wygląda deployment na Heroku, jeden z pierwszej platformie PaaS, która odniosła komercyjny sukces (obecnie część Salesforce). To inżynierowi z Heroku spisali [12factor apps](https://12factor.net/).

1. Załóż konto na [heroku.com](https://www.heroku.com)

2. Będziemy robić deployment prostej aplikacji w Pythonie, którą znajdziesz [py_hello_world](./py_hello_world), uruchom ją według wskazówek w pliku [py_hello_world/README.md](./py_hello_world/README.md).

3. Przekopiuj aplikację i zainicjuj repozytorium gita.

4. Dodaj plik *Procfile*, służy on do przekazania informacji Heroku, jak uruchomić twoją aplikację:

   ```
   web: gunicorn hello:app
   ```

5. Zainstaluj Heroku CLI, korzystając z instrukcji na stronie [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli) 

6. Umieśćmy aplikację na platformie Heroku:

   ```bash
   heroku login -i
   
   # create the app at the heroku side
   heroku create

   # aplikacja pojawi się w heroku dashboard 
   # (przeglądarka internetowa)

   # heroku działa używając git-a:
   git remote -v
   
   # sprawdź czy wszystko jest dodane do gita:
   git status

   # deploy
   git push heroku master

   # w logach zobaczysz url swojej aplikacji
   heroku logs
   ```

## Materiały dodatkowe

- [Cloudflare workers](https://workers.cloudflare.com/) i [Cloudflare Pages](https://blog.cloudflare.com/cloudflare-pages-ga/) - warto poznać
- [AWS CloudFront Lambda@Edge](https://docs.aws.amazon.com/lambda/latest/dg/lambda-edge.html)
- [AWS serverless getting-started](https://aws.amazon.com/serverless/getting-started/)
- https://www.netlify.com/ - również bardzo popularna platforma PaaS
- [Azure Functions Triggers](https://docs.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)
- https://ngrok.com/
