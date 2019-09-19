# Influxdb Support

## docker setting

```
docker network create influxdb
```

## run influxdb

we chose `influxdb:1.3.5`

```
docker run -p 8086:8086 -p 8089:8089/udp \
      --net=influxdb \
      -v $PWD/data/influxdb:/var/lib/influxdb \
      -v $PWD/etc/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
      --name dtl-influxdb \
      influxdb:1.3.5 -config /etc/influxdb/influxdb.conf
```

## run chronograf

we chose `chronograf:1.3.8`

```
docker run -p 8888:8888 \
      --net=influxdb \
      -v $PWD/data/chronograf:/var/lib/chronograf \
      --name dtl-chronograf \
      chronograf:1.3.8 --influxdb-url=http://influxdb:8086
```