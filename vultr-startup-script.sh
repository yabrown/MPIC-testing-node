#!/bin/bash


############# Config for bgp_pathfinder ###########################
echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding=1' >> /etc/sysctl.conf
sysctl -p
apt update
apt install -y bird iperf
ufw disable
####################################################################



############# Config for containerized Polo #######################

ip addr add 66.180.191.1 dev lo

apt install -y docker.io
systemctl start docker

# pull docker containers 
docker pull yabrown/mpic-testing-node:latest
docker pull containrrr/watchtower

# run tutorial container 
docker run -d --name polo -p 80:80 yabrown/mpic-testing-node:latest

# run Watchtower to auto-redeploy container when image is updated
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 30

  ################################################################