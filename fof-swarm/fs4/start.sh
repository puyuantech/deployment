docker pull puyuantech/fof:latest
cd trade1
docker-compose --compatibility up -d
cd ../trade2
docker-compose --compatibility up -d
cd ../trade3
docker-compose --compatibility up -d