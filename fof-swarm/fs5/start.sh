docker pull puyuantech/fof:latest
cd trade4
docker-compose --compatibility up -d
cd ../trade5
docker-compose --compatibility up -d
cd ../trade6
docker-compose --compatibility up -d