#/bin/bash
set -eu

container_name='build'
docker start ${container_name}
docker exec -it ${container_name} bash /shared/code/rebuild_rpm.sh
docker cp ${container_name}:/shared/code/linker/build/ ./resource
docker cp ${container_name}:/shared/code/trader/build/ ./resource
docker cp ${container_name}:/shared/code/crypto-fx/build/ ./resource
docker cp ${container_name}:/shared/code/fof/build/ ./resource
mv ./resource/build/*.rpm ./resource
img_id=$(docker build ./ |  grep built | grep -oE '[^ ]+$')
echo "built docker: ${img_id}"
docker tag ${img_id} testing:latest
