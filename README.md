## A generic Docker Compose file to deploy python apps

Featuring:

- Docker
- Docker Compose
- Docker Machine
- Python
- PostgreSQL
- Mongo
- Traefik

Blog post -> https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/


### Instructions

1. Start new machine - `docker-machine create -d virtualbox dev;`
1. Configure your shell to use the new machine environment - `eval $(docker-machine env dev)`
1. Build images - `docker-compose build`
1. Start services - `docker-compose up -d`
1. Create migrations - `docker-compose run web /usr/local/bin/python manage.py migrate`
1. Grab IP - `docker-machine ip dev` - and view in your browser
