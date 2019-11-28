# Backend deployment using docker-machine on digitalocean
---
Here we are using our bigga docker-compose script to deploy our backend and worker containers on docker-machine. Please follow the below steps to complete the deployment.
#### Steps :-
* you need to crete docker-machine using below command for that you need your digitalocean account api key.
```
docker-machine create --driver digitalocean --digitalocean-access-token=your-token your-machine-name
```
* Clone the bigga repository on your project folder using [reckonsys/bigga](https://github.com/reckonsys/bigga).
* cd into bigga folder, there you can see `docker-compose` file. you need to add the services depends upon you project requirement.
* depends upon your database create the volume and mount in a same services.
Example:
```
volumes:
postgres_data: {}
```
```
services:
  postgres:
    env_file: .env
    restart: always
    image: postgres:latest
    ports:
       - 5432
    volumes:
      - postgres_data:/var/lib/postgresql/data/  
```  
* worker,backend,db,redis,rabbitmq,and traefik, these are all the services must you keep in your docker-compose file.
* If you want another services like websockets and celerybeat, you need to create services for that in your docker-compose file.
 - example: `websockets` you must include below service in your `docker-compose` file.
```
  socket:
       <<: *worker
       command: python sio_server.py
       expose:
         - ${SOCKET_PORT}
       labels:
         - traefik.enable=true
         - traefik.backend.domain=${SOCKET_DOMAIN}
         - traefik.frontend.rule=Host:${SOCKET_DOMAIN}
         - traefik.http.middlewares.testHeader.Headers.AddVaryHeader=true
         - traefik.http.middlewares.testHeader.Headers.AccessControlMaxAge=100
         - traefik.http.middlewares.testHeader.Headers.AccessControlAllowMethods=GET,OPTIONS,PUT,POST,DELETE,PATCH
         - traefik.http.middlewares.testHeader.Headers.AccessControlAllowOrigin=*.${SOCKET_DOMAIN},${SOCKET_DOMAIN}
```
Above `socket` service you must change the command depends upon your project.
 * In our `socket` service we are using `SOCKET_PORT`, it should be come from `.env` file.
 * we are running our `websocket` as a `socket` service in our `docker-compose` file, so it will create a docker container in our server. If you want to access the websocket you must need `SOCKET_DOMAIN` and please make sure your backend configuration depends upon this.
  - you should create a `SOCKET_DOMAIN`name in your DNS, because we are not directly ruunig our `socket` service in our server.
  - create a `A-record` in your DNS using below Example `chat.example.com`.
  ```
  if your docker-machine ip: 192.168.10.8 then your A record will be look like this,
  Host Name: chat
  Type: A record
  Ipv4 address or Data : 192.168.10.8
  ```  
 * `Example:` `clearybeat`  you must include below service in your `docker-compose` file.
 ```
    beat:
      <<: *worker
      command: celery -A tasks.celery beat --loglevel=info
 ```
 Above `beat` service you must change the command depends upon your project.
* we are treafik as a reverse proxy and creating ssl certificate for our domain.

  * please makesure that where you are domian. we need to mention the provider in our `traefik/traefik.toml` file.
  ```
  [acme.dnsChallenge]
  provider = "route53"
  ```
  Please refer the below table and replace the correct provider in your `traefik/traefik.toml` file.
  | DNS           |       Provider      | .ENV                                   |
  |:-------------:|  :-------------:    | :-------------------------------------:|
  | AWS(route53)  | route-53            | AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY|
  | Google        | manual              |         none                           |
  | GoDaddy       | Godaddy             | GODADDY_API_KEY, GODADDY_API_SECRET    |
  | 123Reg        | manual              |         none                           |   
  | Digitalocean  | digitalocean        |       DO_AUTH_TOKEN                    |
  | Namecheap     | namecheap           | NAMECHEAP_API_USER, NAMECHEAP_API_KEY	 |  
  * If you are using above DNS you can create auto ssl and manual ssl creation. if you are using other DNS please refer [traefik-letsencrypt](https://docs.traefik.io/https/acme/).
  * For automatic ssl certificate, you must need to pass the `env` variables form your `.env`.
  * If you are creating manual certificate, you must run below command and get the values from log and add `TXT` record in your dns,but this command you should run after docker-compose up -d.
  ```
  docker-compose --log-level DEBUG run traefik
  ```
  * for adding `TXT` record please follow the below table and kindly replace the value what you got in log.
  |   Hostname      |   Type        |  Destination TXT  |
  |:---------------:| :------------:| :----------------:|
  |_acme_challenge.demo| TXT        | 78373t4891341441  |_   
* create a `.env` file in your bigga folder and add your all env in that file. please refer the below .env example file.

  ```
  APP_MAIL_PASSWORD=test1234
  APP_MAIL_USERNAME=user@example.com
  AWS_ACCESS_KEY_ID=replace_accesskey
  AWS_SECRET_ACCESS_KEY=replace_secretkey
  BACKEND_DOMAIN=api.example.com
  BACKEND_PORT=5000
  BUCKET_NAME=your_frontend_bucketname
  CELERY_BROKER_URL=pyamqp://guest@rabbitmq//
  DISABLE_CORS=0
  DO_AUTH_TOKEN=your_digitalocean_api_key
  DROP_BOX_ACCESS_TOKEN=if_you_need_in_your_project_add_the_env
  FLASK_APP=autoapp.py
  FLASK_ENV=development
  HTTP_PROTOCOL=https://
  MONGO_HOST=mongo
  MONGO_PORT=27017
  POSTGRES_DB=replace_db
  POSTGRES_HOST=postgres
  POSTGRES_PASSWORD=replace_password
  POSTGRES_USER=replace_user_name
  RABBITMQ_HOST=rabbitmq
  REDIS_SOCKET_URL=redis://redis:6379/0
  SECRET_KEY=django_secret_key
  SOCKET_DOMAIN=wsstage.example.com
  SOCKET_PORT=5001
  WORKSPACE_ADMIN_TLD=adminstage.example.com
  WORKSPACE_APP_TLD=appstage.example.com
  VIMEO_ACCESS_TOKEN=replace_access_token_if_you_need_this_env
  VIMEO_CLIENT_ID=replace_client_id_if_you_need_this_env
  VIMEO_CLIENT_SECRET=replace_secretkey_if_you_need_this_env
  ```
* Now you need to create `Dockerfile` and `requirement.txt` in your backend folder. below we are mentioned Dockerfile please use this for your project.
```
FROM python:3.7-alpine
COPY . .
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps alpine-sdk openssl-dev libffi-dev python-dev gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
```  
Mostly we are using these packages in our project, if you neeed aditional packages, add it on our Dockerfile.
* create `requirements.txt` file and add the requirements which you need.
* After completing all the above steps run the below command in `bigga` folder.
```
eval $(docker-machine env yourmachinename)
docker-compose build && docker-compose up -d
```
after this, if you are creating manual certificate, run the treafik loglevel debug command and add the TXT record in yor DNS management.

* Please use the below commands for checking the container state,migrations,logs.
```
docker-compose ps
docker-compose exec worker sh  # to run a migrations inside container
docker-compose logs worker or traefik # for checking logs  
```  
* If incase you need to ssh into a docker-machine, use the below command.
```
docker-machine ssh your machine-name
```
* You can share your docker-machine to your teammates by using machine-share. Please use the below command for machine-share.
```
npm install -g machine-share # for installing machine-share, if incase you are geiing error while installing, use `sudo` with this command
machine-export your-machine-name  # for exporting your machine. it will create your-machine.zip file.
machine-import  your-machine.zip  # for importing machine.
```

* If you want to increase your docker-machine size, goto digitalocean console, stop the machine and resize it. After resize again restart your docker-machine then use it.

##### Addition commad:-
If you want access your database or do some chanegs in database from console, use the below command.

* docker-compose exec postgres sh   # you can enter into postgres container, then run below command
* psql -U postgres   # postgres is your username of the database, then you can list,cretae,delete your database.
