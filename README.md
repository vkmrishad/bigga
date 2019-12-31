## bigga: A generic Docker Compose file to deploy python apps

Featuring:

- Docker
- Docker Compose
- Docker Machine
- Python
- PostgreSQL
- Mongo
- Traefik (nginx alternative)

Blog post -> https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/


### Instructions

1. Start new machine - `docker-machine create -d virtualbox dev;`
1. Configure your shell to use the new machine environment - `eval $(docker-machine env dev)`
1. Build images - `docker-compose build`
1. Start services - `docker-compose up -d`
1. Create migrations - `docker-compose run worker /usr/local/bin/python manage.py migrate` (Please ensure you are not running this command in backend and image that might receive traffic from traefik. Because you don't want a request  to come to this container and fail. )
1. Grab IP - `docker-machine ip dev` - and view in your browser


### Scaling

Suppose you want to run X `backend` containers and Y `worker` containers: `docker-compose scale backend=X worker=Y`


### S3 Based front-end deplotment

Refer our S3 deployment guide: [S3_FRONTEND_DEPLOYMENT.md](S3_FRONTEND_DEPLOYMENT.md)


### Importing / Exporting Docker Machines

Use the `machine-share` npm package. Check out the docs on this GitHub repo: [bhurlow/machine-share](https://github.com/bhurlow/machine-share)


### Troubleshooting

Refer our troubleshooting guide: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)


### Support

Reckonsys offers paid support to containerize your applications (Compose, Swarm, Kubernetes, Mesos, etc..). Please contact [info@reckonsys.com](mailto:info@reckonsys.com) for more details.

# More Docs:

#### [Front-end](https://github.com/reckonsys/bigga/blob/master/docs/Frontend.md)
#### [Backend](https://github.com/reckonsys/bigga/blob/master/docs/Backend.md)
#### [Docker-basics](https://github.com/reckonsys/bigga/blob/master/docs/Docker-container-basics.md)
