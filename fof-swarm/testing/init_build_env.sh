docker run -idt -P --name build -v /shared/code:/shared/code puyuantech/cryptofx
docker cp ./resource/rebuild_rpm.sh build:/shared/code
docker exec -it build chomod +x /shared/code/rebuild_rpm.sh