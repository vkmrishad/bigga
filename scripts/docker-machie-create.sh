# Digital Ocean Sample

# List sizes
doctl compute size list | head

# List regions
doctl compute region list

# Create Machine
docker-machine create \
    --driver digitalocean \
    --digitalocean-access-token $DO_TOKEN \
    --digitalocean-size 4gb \
    --digitalocean-region blr1 \
    myinstance


docker-machine create \
    --driver amazonec2 \
    --amazonec2-access-key $AWS_ACCESS_KEY_ID \
    --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY  \
    --amazonec2-vpc-id $AWS_VPC_ID \
    --amazonec2-region $AWS_DEFAULT_REGION \
    --amazonec2-instance-type a1.xlarge \
    myinstance
