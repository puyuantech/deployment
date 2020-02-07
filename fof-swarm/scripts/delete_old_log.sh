#!/bin/bash
containers=$(docker ps --format "{{.Names}}")
for container in ${containers}
do
    docker exec ${container} /bin/gun log clean -t 8
done