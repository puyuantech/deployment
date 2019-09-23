# CryptoFX 部署文档

## 〇.环境要求

    CentOS 7 (可直接科学上网)

## 一.下载 Docker 镜像

    docker pull puyuantech/cryptofx:latest
    docker pull mysql:latest

## 二.启动容器

### 安装 docker-compose

    pip3 install docker-compose

### 启动容器 (初始化过程大约需要 10 秒)

    docker-compose up -d

## 三.使用 client

### 安装 tlclient

    pip3 install tlclient
    pip3 install pandas
    pip3 install requests

### 测试样例 (market gateway)

运行 Market Gateway Test Client

    python3 scripts/md_test.py

### 测试样例 (trade gateway)

运行 Trade Gateway Test Client

    python3 scripts/td_test.py
