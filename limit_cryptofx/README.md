# 闪兑系统单机 docker-compose 分布式部署指南

# install docker-compose

    curl -L https://github.com/docker/compose/releases/download/1.25.1-rc1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

## run

    docker-compose --compatibility up -d

## stop

    docker-compose --compatibility down
