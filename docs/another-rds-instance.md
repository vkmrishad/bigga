# How to migrate your data from an existing RDS instance to the new RDS instance.
---

If you are looking to move your data from one RDS instance to another, you are on the just right place. Below we will see how do we create new RDS instance on amazon AWS and move the data from the old one to new one.

1. First of all create a new RDS instance in aws with the same VPN as your old one, Probably keep all the below same as your old one. With the configuration your application requires.

* Database name,
* Database user,
* Database password.

Once we have the database created.

2. Let's take dump of the existing database.

* In order to take dump before we need to bash into Worker
```
docker-compose exec backend bash
```
* Once you are in bash. You will need to take pg_dump which needs pgclient, Let's install it.
```
apt update
apt-get install postgresql-client
```
* Now you will have postgresql client in that container. Now we need to take pg_dump with this command.
```
pg_dump --column-inserts --data-only -h <public dns> -U <username> <database> > dumpfile.sql
```
* It should now prompt for password, use the password set for the instance ( Can be found in env file )
* So once it terminates, we should now a database dump in the specified path.

3. So, Next let's load the dump to the new RDS instance.

* First we need to export the new <host> by, to connect to the database in docker instance locally ( Don't worry it won't read from the new database directly before we do docker-build and up -d).
```
export DATABASE_HOST=<new public dns>
```
* Once we are done with this run migrations on the new database.
```
./manage.py migrate
```
* Then let's now try to connect to the new database instance using pg command.
```
psql -h <new public dns> -U <username>
```
* It will again prompt for password. Once we enter into the postgres instance, just make sure we don't have any data. By doing `\dt`.
* Once your in the psql console, just run this to load the data.
```
\i /dumpfile.sql
```

4. So we once we get the prompt, we should have loaded the dumpfile to the new database. Just make sure by checking count of some frequently updated table.

5. After that change the `old endpoint` in the `env` to `new endpoint`.
6. Then do `docker-compose build` and `docker-compose up -d`. Check for the changes on your application, if api's are working fine. If not probably to `docker-compose down` and `docker-compose up -d`
