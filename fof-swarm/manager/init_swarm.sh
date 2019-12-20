# firewall-cmd --add-port 2377/tcp
# firewall-cmd --add-port 7946/tcp
# firewall-cmd --add-port 7946/udp
# firewall-cmd --add-port 4789/udp

docker swarm init
docker network create -d overlay --attachable fof-swarm
docker swarm join-token worker
