# !/bin/bash

apt-get update -y
apt-get install -y docker.io
systemctl start docker

# pull docker containers 
docker pull christineguoo/docker-tutorial:latest
docker pull containrrr/watchtower

# run tutorial container 
docker run -d -p 5000:5000 christineguoo/docker-tutorial:latest

# run Watchtower to auto-redeploy container when image is updated
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 30
