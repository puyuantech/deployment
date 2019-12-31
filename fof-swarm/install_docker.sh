# docker
yum install docker -y && systemctl start docker && systemctl enable docker
# docker compose
curl -L https://github.com/docker/compose/releases/download/1.25.1-rc1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose &&ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose