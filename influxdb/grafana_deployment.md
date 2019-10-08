# Grafana Deployment

## docker setting

```
docker network create traderslink
```

## run influxdb

we chose `influxdb:1.3.5`

```
docker run -d -p 8086:8086 -p 8089:8089/udp \
      --net=traderslink \
      -v $PWD/data/influxdb:/var/lib/influxdb \
      -v $PWD/etc/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
      --name dtl-influxdb \
      influxdb:1.3.5 -config /etc/influxdb/influxdb.conf
```

## run grafana

we chose `grafana/grafana:latest`

```
docker run -d -p 3000:3000 \
      --net=traderslink \
      -v $PWD/data/grafana:/var/lib/grafana \
      --name dtl-grafana \
      grafana/grafana:latest
```

## run main

we chose `puyuantech/cryptofx:latest`

```
docker run -d -it -p 9000-9007:9000-9007 \
      --net=traderslink \
      -v $PWD/data/main:/shared \
      --name dtl-main \
      puyuantech/cryptofx:latest
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
```

run md_client to subscribes

## grafana setting

    http://localhost:3000

### login:

    admin
    admin

### add data source:

    influxdb setting:
    URL: http://dtl-influxdb:8086
    Database: trader

### add dashboard:

    panel test setting:
    select ask_price1, ask_price2, bid_price1, bid_price2 from MktSnapOpt where ticker = 'btc/usdt' and exchange = '103'
    select open, high, low, close from MktBarGen where ticker = 'btc/usdt' and exchange = '103'
    select price from MktTrade where ticker = 'btc/usdt' and exchange = '103'
