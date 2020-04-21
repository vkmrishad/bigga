# Troubeleshooting


1. If docker build takes too long, make sure there is a [`.dockerignore`](.dockerignore) file. Make sure you are ignoring `.git/`, `media/`, `upload/`, virtualenvs and all files and folders that you do not need for the deployment.
1. **NEVER** leave a shell command open for too long (for example: `docker-compose exec worker python manage.py shell`). When you open interactive shell to do something, do it & exit immedietly. Our app might misbehave when there is a lot of interactive shells open because it creates multiple DB containers for each of your session and this is somehow resulting in weird errors that cannot be replicated locally (possibly happening due to mouting same volume on multiple DB containers).
1. Kill zombie docker processes. run `python zombie.py` to see a list of **possible** zombie container IDs. And run `docker kill <list-of-container-ids>` to kill all the zombie processes.
1. Run `docker system prune`. Sometimes old images might take too many space. Its probably a good idea to clear them out once in a while.
1. I don't know if there are any other issues. If these steps did not solve your issue, let us know.
1. `export COMPOSE_TLS_VERSION=TLSv1_2` is your docker commads are throwing TLS error
