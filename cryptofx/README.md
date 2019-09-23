# CryptoFX 部署文档

## 一.下载 Docker 镜像

    docker pull puyuantech/cryptofx
    docker pull mysql

## 二.启动容器

    docker run -d -it -p 9000-9007:9000-9007 -v /shared:/shared --name cryptofx puyuantech/cryptofx
    docker run -d -it -p 3306:3306 -v /shared/mysql/logs:/logs -v /shared/mysql/conf:/etc/mysql/conf.d -v /shared/mysql/data:/var/lib/ -e MYSQL_ROOT_PASSWORD=puyuantech --name mysql mysql

## 三.目录结构

    |—— shared
    |   |—— etc
    |   |   └── config.json
    |   |—— log
    |   |—— mysql
    |   |   |—— conf
    |   |   |—— data
    |   |   └── logs

在 config.json 中配置好数据库信息。
```json
"database": {
    "development": {
        "username": "root",
        "xport": 3306,
        "db": "db_core",
        "host": "${HOST}",
        "password": "${PASSWORD}",
        "port": 3306
    },
    "mode": "development"
},
```

    快速查看容器 ip:
    docker inspect -f '{{.Name}} - {{.NetworkSettings.IPAddress}}' $(docker ps -aq)

config.json 测试示例：
```json
{
    "master_rep": "tcp://0.0.0.0:9000",
    "config_version": "0.3",
    "gateway_reconnection_policy": {
        "max_retry_times": 20,
        "notification_methods": {
            "email": "",
            "slack": ""
        },
        "retry_interval_in_seconds": 5
    },
    "env": "env1",
    "master_rep_port": 9000,
    "modules": [
        {
            "fist_type": "MASTER",
            "fist_name": "master",
            "addrs": {
                "Zmq_PUB": {
                    "comm_method": "TCP",
                    "port": 9001
                },
                "Zmq_REP": {
                    "comm_method": "TCP",
                    "port": 9000
                }
            },
            "source_id": 0
        },
        {
            "fist_type": "MARKET_ROUTER",
            "fist_name": "market1",
            "addrs": {
                "Zmq_PULL": {
                    "comm_method": "TCP",
                    "port": 9002
                },
                "Zmq_PUB": {
                    "comm_method": "TCP",
                    "port": 9004
                },
                "Zmq_REP": {
                    "comm_method": "TCP",
                    "port": 9003
                }
            },
            "source_id": 1
        },
        {
            "fist_type": "TRADE_ROUTER",
            "fist_name": "trade1",
            "addrs": {
                "Zmq_PULL": {
                    "comm_method": "TCP",
                    "port": 9005
                },
                "Zmq_PUB": {
                    "comm_method": "TCP",
                    "port": 9007
                },
                "Zmq_REP": {
                    "comm_method": "TCP",
                    "port": 9006
                }
            },
            "source_id": 2
        },
        {
            "fist_type": "BASKET_SERVER",
            "fist_name": "basket",
            "source_id": 3
        },
        {
            "fist_type": "ALGO_SERVER",
            "fist_name": "twap",
            "source_id": 4
        },
        {
            "fist_type": "RISK_MANAGER",
            "fist_name": "rms1",
            "source_id": 5
        },
        {
            "fist_type": "ORDER_MANAGER",
            "fist_name": "oms1",
            "source_id": 6
        }
    ],
    "accounts": {
    },
    "env_infos": [
        {
            "public_ip": "127.0.0.1",
            "env_name": "env1",
            "private_ip": "0.0.0.0"
        },
        {
            "public_ip": "127.0.0.1",
            "env_name": "env2",
            "private_ip": "0.0.0.0"
        }
    ],
    "notification_center": {
        "redis_backup": {
            "host": "127.0.0.1",
            "port": 6379,
            "password": "",
            "key": "notification"
        }
    },
    "database": {
        "development": {
            "username": "root",
            "xport": 3306,
            "db": "db_core",
            "host": "172.17.0.3",
            "password": "puyuantech",
            "port": 3306
        },
        "mode": "development"
    }
}
```

## 四.进入 cryptofx 容器

    docker exec -it cryptofx bash

由于 trade、linker 更新原因，可能有以下包未安装：

    sqlalchemy
    cryptography

可以使用 pip 命令快速安装：

    pip3 install sqlalchemy
    pip3 install cryptography

### 1.初始化数据库

    gun db create && gun db init

### 2.启动 master、router

    gun start master
    gun start mr -f market1
    gun start tr -f trade1

### 3.启动 market gateway (默认 -r market1)

    gun run mg -g binance -p cryptofx
    gun run mg -g bitmex -p cryptofx
    gun run mg -g huobi -p cryptofx
    gun run mg -g okex -p cryptofx

将 gun run 用 gun start 代替，可后台运行。

### 4.配置账户信息

使用加密

    生成密钥对，作为 default_key。
    添加账户信息：
    gun account new -a ${ACCOUNT_NAME} -k default_key -c access_key:${YOUR_ACCESS_KEY} secret_key:{YOUR_SECRET_KEY}

不使用加密 (测试用)

    添加账户信息：
    gun account new -a ${ACCOUNT_NAME} -c access_key:${YOUR_ACCESS_KEY} secret_key:{YOUR_SECRET_KEY}

可以查询当前已经保存的账户信息：

    gun account list

### 5.启动 trade gateway (默认 -r trade1)

    gun run tg -g binance -a ${ACCOUNT_NAME} -p cryptofx
    gun run tg -g bitmex -a ${ACCOUNT_NAME} -p cryptofx
    gun run tg -g huobi -a ${ACCOUNT_NAME} -p cryptofx
    gun run tg -g okex -a ${ACCOUNT_NAME} -p cryptofx

## 五.使用 client

### 安装 tlclient

    pip3 install tlclient

由于 trade、linker 更新原因，可能有以下包未安装：

    pandas
    requests

可以使用 pip 命令快速安装：

    pip3 install pandas
    pip3 install requests

### 测试样例 (market gateway)

```python
from tlclient.trader.client import Client
from tlclient.trader.constant import ExchangeID

class MdTest(Client):

    def __init__(self):
        Client.__init__(self, name='md_test', env_name='mac1', addr="tcp://localhost:9000")
        self.init_market('market1')
        self.init_trade('trade1')

    def on_mkt_trade(self, obj, msg_type, frame_nano):
        print('[on_mkt_trade] (msg_type){} (obj){}'.format(msg_type, obj))

    def on_mkt_bar(self, obj, msg_type, frame_nano):
        print('[on_mkt_bar] (msg_type){} (obj){}'.format(msg_type, obj))

    def on_mkt_snap(self, obj, msg_type, frame_nano):
        print('[on_mkt_snap] (msg_type){} (obj){}'.format(msg_type, obj))

if __name__ == '__main__':
    md = MdTest()
    md.subscribe_trade(ExchangeID.HUOBI, "btc/usdt")
    md.subscribe_bar(ExchangeID.HUOBI, "btc/usdt")
    md.subscribe_snap(ExchangeID.HUOBI, "btc/usdt")
    md.start()
    md.join()
```

### 测试样例 (trade gateway)

```python

from tlclient.trader import message_trade
from tlclient.trader.client import Client
from tlclient.trader.constant import AssetType, Direction, ExchangeID, OffsetFlag, OrderType

class MdTest(Client):

    def __init__(self):
        Client.__init__(self, name='md_test', env_name='mac1', addr="tcp://localhost:9000")
        self.init_market('market1')
        self.init_trade('trade1')

    def on_rsp_order_insert(self, obj: message_trade.RspOrderInsert, frame_nano):
        self.logger.info('[roi] (obj){}'.format(obj))

    def on_rsp_order_cancel(self, obj: message_trade.RspOrderCancel, frame_nano):
        self.logger.info('[roc] (obj){}'.format(obj))

    def on_rtn_trade(self, obj: message_trade.RtnTrade, frame_nano):
        self.logger.info('[rtt] (obj){}'.format(obj))

    def on_rtn_order(self, obj: message_trade.RtnOrder, frame_nano):
        self.logger.info('[rto] (obj){}'.format(obj))

    def on_rsp_position(self, obj: message_trade.RspPosition, frame_nano):
        self.logger.info('[pos] (obj){}'.format(obj))

if __name__ == '__main__':
    md = MdTest()

    md.insert_order('pybm', ExchangeID.BITMEX, 'xbtusd', -1, 3, OrderType.MARKET, Direction.SELL, asset_type=AssetType.CRYPTO_CONTRACT, offset_flag=OffsetFlag.OPEN)

    oid = md.insert_order('pybm', ExchangeID.BITMEX, 'xbtusd', 7000, 5, OrderType.LIMIT, Direction.BUY, asset_type=AssetType.CRYPTO_CONTRACT, offset_flag=OffsetFlag.OPEN)
    if oid == -1:
        print('order insert error.')
    else:
        md.cancel_order(oid, 'pybm')

    md.req_position('pybm')

    md.start()
    md.join()
```
