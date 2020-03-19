# 托管机远程运维部署文档

## 一.本地机器准备

### 下载 Docker 镜像

    docker pull puyuantech/traderslink-0.5:latest

### 启动容器

    docker run -d -it -p 9000-9007:9000-9007 -p 20202:20202 --name traderslink puyuantech/traderslink-0.5:latest

### 进入容器

    docker exec -it traderslink bash

### 查看 ip

    >> gun ip
    current public ip:  11.111.111.111

### 安装 tmux

    yum install -y tmux

## 二.远程机器准备

### 下载 Docker 镜像

    docker pull puyuantech/traderslink-0.5:latest

### 启动容器

    docker run -d -it --name traderslink puyuantech/traderslink-0.5:latest

### 进入容器

    docker exec -it traderslink bash

### 查看 ip

    >> gun ip
    current public ip:  22.222.222.222

### 修改配置文件

    在 "accounts" 中配置好账户信息。
    使用以下配置覆盖 /shared/etc/config.json:
    {
        "master_rep": "tcp://11.111.111.111:9000",
        "master_rep_port": 9000,
        "env": "env2",
        "gateway_reconnection_policy": {
            "max_retry_times": 20,
            "retry_interval_in_seconds": 5
        },
        "accounts": {}
    }

### 安装 tmux

    yum install -y tmux

### 使用 tmux 后台运行远程服务

    tmux new -s traderslink
    gun remote run -s executor -H 11.111.111.111

## 三.本地机器配置

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
                "public_ip": "11.111.111.111",
                "env_name": "env1",
                "private_ip": "11.111.111.111"
            },
            {
                "public_ip": "22.222.222.222",
                "env_name": "env2",
                "private_ip": "22.222.222.222"
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
        }
    }

### 正常启动 master、行情路由和交易路由

    gun start master
    gun start mr -f market1
    gun start tr -f trade1

### 安装 tmux

    yum install -y tmux

### 使用 tmux 后台运行远程服务

    tmux new -s traderslink
    gun remote run -s dispatcher

### 使用远程服务启动交易网关

    例如:
    gun remote exec -c 'gun start mg -a xtp_market -g xtp'
    gun remote exec -c 'gun start tg -a xtp_trade -g xtp'
