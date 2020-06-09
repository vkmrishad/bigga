# DROP and CREATE a new DB on RDS

1. Connect with RDS: `psql -h amazon-rds-endpoint.com -U awsuser -d postgres`
2. Run `DROP DATABASE database_name`
3. run `CREATE DATABASE database_name WITH OWNER OWNER_USER`

If your RDS instance is not publically accessibe:

Run `docker-compose exec postgres sh` to open postgres shell and the run the above commands
