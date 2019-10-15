# CryptoFX Trade Server

## 配置服务
### 配置 MySQL
```
docker pull mysql  
docker run -d -it -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password --name mysql mysql
```

### 启动 CFX Docker
```
docker pull puyuantech/cryptofx  
docker run -d -it -p 13624:13624 -v ~/Github/:/shared --name cryptofx puyuantech/cryptofx  
docker exec -it cryptofx bash
```

### 配置 CFX trade server 环境
```
mkdir -p /shared/cfx/log  
mkdir -p /shared/cfx/etc  
cp /shared/crypto-fx/rpm/etc/config.json /shared/cfx/etc/
```

### 配置 CFX 数据库，插入测试数据
```
cd /shared/crypto-fx/python/  
python3 -m cryptofx.cfx_trader setupdb  
python3 -m cryptofx.cfx_trader reset_test_data
```

### 启动 CFX trade server
```
cd /shared/crypto-fx/python/  
python3 -m cryptofx.cfx_trader ser
```

## 接口说明
### 查询可交易币对
[GET] http://localhost:13624/api/v1/market-data/symbols
#### response
Available symbol list
```json
{
    "data":[
        "test_a/test_b"
    ],
    "err_msg": null,
    "msg": null
}
```

### 查询币对详情
[POST] http://localhost:13624/api/v1/market-data/symbol-detail
#### request
|param|value|type|
|:-:|:-:|:-:|
|symbol|requested symbol|string|
```json
{
    "symbol": "test_a/test_b"
}
```
#### response
|param|value|type|
|:-:|:-:|:-:|
|ask|ask prices and volumes|pair of doubles|
|bid|ask prices and volumes|pair of doubles|
|symbol|symbol|string|
|mkt_time|market time|string|
```json
{
    "data": {
        "ask": [
            {
                "price": 11,
                "volume": 1
            },
            {
                "price": 12,
                "volume": 2
            },
            {
                "price": 13,
                "volume": 3
            },
            {
                "price": 14,
                "volume": 4
            },
            {
                "price": 15,
                "volume": 5
            },
            {
                "price": 16,
                "volume": 6
            },
            {
                "price": 17,
                "volume": 7
            },
            {
                "price": 18,
                "volume": 8
            },
            {
                "price": 19,
                "volume": 9
            },
            {
                "price": 20,
                "volume": 10
            }
        ],
        "bid": [
            {
                "price": 10,
                "volume": 1
            },
            {
                "price": 9,
                "volume": 2
            },
            {
                "price": 8,
                "volume": 3
            },
            {
                "price": 7,
                "volume": 4
            },
            {
                "price": 6,
                "volume": 5
            },
            {
                "price": 5,
                "volume": 6
            },
            {
                "price": 4,
                "volume": 7
            },
            {
                "price": 3,
                "volume": 8
            },
            {
                "price": 2,
                "volume": 9
            },
            {
                "price": 1,
                "volume": 10
            }
        ],
        "mkt_time": "2019/10/09 16:01:51",
        "symbol": "test_a/test_b"
    },
    "err_msg": null,
    "msg": null
}
```

### 查询持仓
[POST] http://localhost:13624/api/v1/trade/position
#### request
|param|value|type|
|:-:|:-:|:-:|
|account|requested account|string|
```json
{
    "account": "cfx_acc"
}
```
#### response
|param|value|type|
|:-:|:-:|:-:|
|account_id|account id|string|
|symbol|position symbol|string|
|volume|position volume|double|
```json
{
    "data": [
        {
            "account_id": "cfx_acc",
            "symbol": "test_a",
            "volume": 9996.0
        },
        {
            "account_id": "cfx_acc",
            "symbol": "test_b",
            "volume": 10044.5
        }
    ],
    "err_msg": null,
    "msg": null
}
```

### 下单
[POST] http://localhost:13624/api/v1/trade/place-order
#### request
|param|value|type|
|:-:|:-:|:-:|
|account|client account|string|
|symbol|trading symbol|string|
|price|trading price (LIMIT order)|double|
|volume|trading volume|double|
|order_type|11 (LIMIT) / 12 (MARKET)|int|
|direction|1 (BUY) / 2 (SELL)|int|
```json
{
    "account": "user_a",
    "symbol": "test_a/test_b",
    "price": 11.5,
    "volume": 1,
    "order_type": 11,
    "direction": 1
}
```
#### response
|param|value|type|
|:-:|:-:|:-:|
|price|traded price|double|
|volume|traded volume|double|
```json
{
    "data": {
        "price": 11.5,
        "volume": 1
    },
    "err_msg": null,
    "msg": null
}
```