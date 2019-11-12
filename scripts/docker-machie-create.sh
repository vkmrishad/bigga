# Digital Ocean Sample

# List sizes
doctl compute size list | head

# List regions
doctl compute region list

# Create Machine
docker-machine create \
    --driver digitalocean \
    --digitalocean-access-token <TOKEN> \
    --digitalocean-size 512mb \
    --digitalocean-region blr1 \
    myinstance
