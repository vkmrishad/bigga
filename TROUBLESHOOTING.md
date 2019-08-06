# Troubeleshooting


## It takes a lot of time to run `docker-compose build`

1. Make sure there is a [`.dockerignore`](.dockerignore) file. Make sure you are ignoring `.git/`, `media/`, `upload/`, virtualenvs and all files and folders that you do not need for the deployment.
2. run `docker system prune`. Sometimes old images might take too many space. Its probably a good idea to clear them out once in a while.
3. I don't know if there are any other issues. If both of these did not solve your issue, let us know.
