# 闪兑系统单机部署指南

## 组件

    1.influxdb
    2.mysql
    3.grafana
    4.cryptofx(包含recoder)

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

## run mysql

we chose `mysql:latest`

```
docker run -d -it \
    -p 3306:3306 \
    --net=traderslink \
    -v $PWD/data/mysql/logs:/logs \
    -v $PWD/data/mysql/conf:/etc/mysql/conf.d \
    -v $PWD/data/mysql/data:/var/lib \
    -e MYSQL_ROOT_PASSWORD=puyuantech \
    --name dtl-mysql \
    mysql:latest
```

## run grafana

we chose `grafana/grafana:latest`

```
docker run -d \
    --user root \
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
sh ./data/influxdb/scripts/init-influxdb.sh
```

## dtl-main setting

```
# init mysql
gun db create && gun db init
# run cryptofx
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
    2.mysql
    3.grafana
    4.cryptofx(不包含recoder)
    5.recoder

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

## run mysql

we chose `mysql:latest`

```
docker run -d -it \
    -p 3306:3306 \
    -v $PWD/data/mysql/logs:/logs \
    -v $PWD/data/mysql/conf:/etc/mysql/conf.d \
    -v $PWD/data/mysql/data:/var/lib \
    -e MYSQL_ROOT_PASSWORD=puyuantech \
    --name dtl-mysql \
    mysql:latest
```

## run grafana

we chose `grafana/grafana:latest`

```
docker run -d \
    --user root \
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
sh ./data/influxdb/scripts/init-influxdb.sh
```

## dtl-main setting

```
# update config.json
database -> development -> host
should update to {dtl-mysql-host}
```

```
# init mysql
gun db create && gun db init
# run cryptofx
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
gun start rr --rt influxdb --host {dtl-influxdb-host} --port 8086
```
