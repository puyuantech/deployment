# 托管机远程运维部署文档

## 一.本地机器配置

### 下载 Docker 镜像

    docker pull puyuantech/traderslink-0.5:latest

### 启动容器

    docker run -d -it -p 9000-9007:9000-9007 -p 20202:20202 --name traderslink puyuantech/traderslink-0.5:latest

### 进入容器

    docker exec -it traderslink bash

### 查看本机 ip

    >> gun ip
    current public ip:  11.111.111.111

### 修改配置文件

    在 /shared/etc/config.json 文件中找到 "env_infos",
    将 "env_infos" 中 "env_name" 为 "env1" 所在项的 "public_ip" 改为本机 ip (默认为 "127.0.0.1")
    例如:
    {
        ......
        "env_infos": [
            {
                "public_ip": "11.111.111.111",
                "env_name": "env1",
                "private_ip": "127.0.0.1"
            }
        ],
        ......
    }

### 正常启动 master、行情路由和交易路由

    gun start master
    gun start mr -f market1
    gun start tr -f trade1

### 在后台运行远程服务

    gun remote run -s dispatcher &

## 二.远程托管机器配置

### 下载 Docker 镜像

    docker pull puyuantech/traderslink-0.5:latest

### 启动容器

    docker run -d -it --network=host -v ~/config.json:/shared/etc/config.json -v ~/log:/shared/log --name traderslink puyuantech/traderslink-0.5:latest

### 进入容器

    docker exec -it traderslink bash

### 修改配置文件

    在 "accounts" 中配置好账户信息。(需要配置 user_id、password 和 key)
    使用以下配置覆盖 /shared/etc/config.json:
    {
        "master_rep": "tcp://11.111.111.111:9000",
        "master_rep_port": 9000,
        "env": "env2",
        "gateway_reconnection_policy": {
            "max_retry_times": 20,
            "retry_interval_in_seconds": 5
        },
        "accounts": {
            "xtp_trade": {
                "gateway_type": "TRADE_GATEWAY",
                "gateway_name": "xtp",
                "client_id": ,
                "file_path": "./xtp_files",
                "user_id": "",
                "password": "",
                "key": "",
                "server_ip": "",
                "server_port": ,
                "hb_interval": 5
            },
            "xtp_market": {
                "gateway_type": "MARKET_GATEWAY",
                "gateway_name": "xtp",
                "user_id": "",
                "password": "",
                "quote_ip": "",
                "quote_port": ,
                "file_path": "./xtp_files"
            }
        }
    }

### 在后台运行远程服务

    gun remote run -s executor -H 11.111.111.111 &

## 三.本地机器通过远程命令在远程托管机上启动网关

### 启动网关

    例如:
    gun remote exec -c 'gun start mg -a xtp_market -g xtp'
    gun remote exec -c 'gun start tg -a xtp_trade -g xtp'

### 使用 Linux 命令查看远程托管机状态等

    例如：
    gun remote exec -c 'ps aux'

注: 不能使用 `top` 这种持续刷新的命令。
