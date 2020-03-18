# 文件扫单部署文档

## 〇.环境要求

    Windows 10 Pro
    Python 3.7

## 一.容器配置

### 下载 Docker 镜像

    docker pull puyuantech/traderslink-0.5:latest

### 启动容器

    docker run -d -it -p 9000-9007:9000-9007 --name traderslink puyuantech/traderslink-0.5:latest

### 进入容器

    docker exec -it traderslink bash

### 修改配置文件

    使用以下配置覆盖 /shared/etc/config.json:
    {
        "config_version": "0.3",
        "master_rep": "tcp://0.0.0.0:9000",
        "master_rep_port": 9000,
        "env": "env1",
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
            }
        ],
        "env_infos": [
            {
                "public_ip": "127.0.0.1",
                "env_name": "env1",
                "private_ip": "127.0.0.1"
            },
            {
                "public_ip": "127.0.0.1",
                "env_name": "env2",
                "private_ip": "127.0.0.1"
            }
        ],
        "gateway_reconnection_policy": {
            "max_retry_times": 20,
            "retry_interval_in_seconds": 5
        },
        "notification_center": {
            "slack": "",
            "redis": {
                "host": "",
                "port": 6379,
                "password": "",
                "key": "notification"
            }
        },
        "database": {
            "development": {
                "username": "",
                "xport": 3306,
                "db": "",
                "host": "",
                "password": "",
                "port": 3306
            },
            "mode": "development"
        },
        "accounts": {}
    }

### 启动 master 和交易路由

    gun start master
    gun start tr -f trade1

## 二.交易网关配置

### 安装 Python 依赖包

    pip install tlclient==0.5.3
    pip install requests
    pip install pandas

### 请联系 Puyuan Tech 获取 impl-pytg

    解压 impl-pytg 压缩包

### 账户配置

在 `impl-pytg/python/gateways/xyzq/tg_xyzq.py` 文件最后

    填入 `account_id`(资金账户) 和 `file_dir`(指令文件目录)。
    指令文件目录要求与扫单程序的指令文件目录一致。

`file_dir` 填写格式为 `'c:\\code\\xyzq'` 或者 `r'c:\code\xyzq'` 或者 `'c:/code/xyzq'`

### 日志文件配置

可以通过配置环境变量 `CONSOLE_LOG_LEVEL` 为 `error`、`warning`、`info`、`debug` 等来查看不同输出级别的控制台 log。(默认为 `error`)

可以通过配置环境变量 `FILE_LOG_LEVEL` 为 `error`、`warning`、`info`、`debug` 等来查看不同输出级别的文件 log。(默认为 `info`)

可以通过配置环境变量 `FILE_LOG_PATH` 来指定文件 log 的存储路径。(默认为 `c:/tmp/linker/log`)

### 启动扫单程序，开启指令订单模式

### 启动交易网关

在 `impl-pytg/python` 目录下执行 `python -m gateways.xyzq.tg_xyzq` 即可。

## 三.测试

在 `impl-pytg/scripts/trading` 目录下配置了一些测试脚本，可以用来测试下单、撤单、查账户、查持仓、查全量订单和查全量成交等。
