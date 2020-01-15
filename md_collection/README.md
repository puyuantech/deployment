# CryptoFX 行情收集系统

## 数据库配置

### InfluxDB

    docker run -d --network host -v $PWD/influxdb:/var/lib/influxdb -v $PWD/etc/influxdb.conf:/etc/influxdb/influxdb.conf:ro --name dtl-influxdb influxdb:1.7.8 -config /etc/influxdb/influxdb.conf
    sh influxdb/scripts/init-influxdb.sh

### Redis

    docker run -d -it --network host --name dtl-redis redis --requirepass "{YOUR_REDIS_PASSWORD}"

## Grafana 配置

    docker run -d --user root -p 3000:3000 --network host -v $PWD/grafana:/var/lib/grafana --name dtl-grafana grafana/grafana:latest

## Docker Compose 分布式部署

### install docker-compose

    curl -L https://github.com/docker/compose/releases/download/1.25.1-rc1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

### run

    docker-compose --compatibility up -d

### stop

    docker-compose --compatibility down
