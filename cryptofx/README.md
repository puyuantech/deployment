# 闪兑系统单机部署指南

## 组件

    1.influxdb
    2.grafana
    3.cryptofx(包含recoder)

## docker setting

```
docker network create traderslink
```

## run influxdb

we chose `influxdb:1.7.8`

```
docker run -d \
    -p 8086:8086 \
    -p 8089:8089/udp \
    --net=traderslink \
    -v $PWD/data/influxdb:/var/lib/influxdb \
    -v $PWD/etc/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
    --name dtl-influxdb \
    influxdb:1.7.8 \
    -config /etc/influxdb/influxdb.conf
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

we chose `puyuantech/cryptofx:latest`

```
docker run -d -it \
    -p 9000-9007:9000-9007 \
    --net=traderslink \
    -v $PWD/data/main:/shared \
    --name dtl-main \
    puyuantech/cryptofx:latest
```

## dtl-influxdb setting

init trader database
```
docker exec dtl-influxdb sh "/var/lib/influxdb/init-influxdb.sh"
```

## dtl-main setting

```
gun start master
gun start mr -f market1
gun start mg -g binance -p cryptofx
gun start mg -g bitmex -p cryptofx
gun start mg -g huobi -p cryptofx
gun start mg -g okex -p cryptofx
gun start rr --rt influxdb --host dtl-influxdb --port 8086
python3 /shared/scripts/md_test.py
```

# 闪兑系统分布式部署指南

## 组件

    1.influxdb
    2.grafana
    3.cryptofx(不包含recoder)
    4.recoder

## run influxdb

we chose `influxdb:1.7.8`

```
docker run -d \
    -p 8086:8086 \
    -p 8089:8089/udp \
    -v $PWD/data/influxdb:/var/lib/influxdb \
    -v $PWD/etc/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
    --name dtl-influxdb \
    influxdb:1.7.8 \
    -config /etc/influxdb/influxdb.conf
```

## run grafana

we chose `grafana/grafana:latest`

```
docker run -d \
    --user $(id -u) \
    -p 3000:3000 \
    -v $PWD/data/grafana:/var/lib/grafana \
    --name dtl-grafana \
    grafana/grafana:latest
```

## run main

we chose `puyuantech/cryptofx:latest`

```
docker run -d -it \
    -p 9000-9007:9000-9007 \
    -v $PWD/data/main:/shared \
    --name dtl-main \
    puyuantech/cryptofx:latest
```

## run recoder

we chose `puyuantech/cryptofx:latest`

```
docker run -d -it \
    -v $PWD/data/main:/shared \
    --name dtl-recoder \
    puyuantech/cryptofx:latest
```

## dtl-influxdb setting

init trader database
```
docker exec dtl-influxdb sh "/var/lib/influxdb/init-influxdb.sh"
```

## dtl-main setting

```
gun start master
gun start mr -f market1
gun start mg -g binance -p cryptofx
gun start mg -g bitmex -p cryptofx
gun start mg -g huobi -p cryptofx
gun start mg -g okex -p cryptofx
python3 /shared/scripts/md_test.py
```

## dtl-recoder setting

```
gun start rr --rt influxdb --host dtl-influxdb --port 8086
```
