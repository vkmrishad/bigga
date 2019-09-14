# Troubeleshooting


## It takes a lot of time to run `docker-compose build`

1. Make sure there is a [`.dockerignore`](.dockerignore) file. Make sure you are ignoring `.git/`, `media/`, `upload/`, virtualenvs and all files and folders that you do not need for the deployment.
1. Kill zombie docker processes. run `python zombie.py` to see a list of **possible** zombie container IDs. And run `docker kill <list-of-container-ids>` to kill all the zombie processes
1. Run `docker system prune`. Sometimes old images might take too many space. Its probably a good idea to clear them out once in a while.
1. I don't know if there are any other issues. If both of these did not solve your issue, let us know.
