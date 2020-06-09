# DROP and CREATE a new DB on RDS

1. Connect with RDS: `psql -h amazon-rds-endpoint.com -U postgres -d postgres`
2. Run `DROP DATABASE database_name`
3. run `CREATE DATABASE database_name [with owner owner_name]`

If your RDS instance is not publically accessibe:

Run `docker-compose exec postgres sh` to open postgres shell and the run the above commands
