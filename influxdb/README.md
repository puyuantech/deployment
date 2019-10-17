# Influxdb Support

## docker setting

```
docker network create traderslink
```

## run influxdb

we chose `influxdb:1.3.5`

```
docker run -d \
    -p 8086:8086 \
    -p 8089:8089/udp \
    --net=traderslink \
    -v $PWD/data/influxdb:/var/lib/influxdb \
    -v $PWD/etc/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
    --name dtl-influxdb \
    influxdb:1.3.5 -config /etc/influxdb/influxdb.conf
```

## run chronograf

we chose `chronograf:1.3.8`

```
docker run \
    -p 8888:8888 \
    --net=traderslink \
    -v $PWD/data/chronograf:/var/lib/chronograf \
    --name dtl-chronograf \
    chronograf:1.3.8 --influxdb-url=http://dtl-influxdb:8086
```

## run grafana

we chose `grafana/grafana:latest`

```
docker run -d \
    --user $(id -u) \
    -p 3000:3000 \
    --net=traderslink \
    -v $PWD/data/grafana:/var/lib/grafana \
    --name dtl-grafana \
    grafana/grafana:latest
```

## run main

we chose `puyuantech/cryptofx:latest` or `puyuantech/traderslink:latest`

```
docker run -d -it \
    -p 9000-9007:9000-9007 \
    --net=traderslink \
    -v $PWD/data/main:/shared \
    --name dtl-main \
    puyuantech/cryptofx:latest
```
