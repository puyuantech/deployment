#!/bin/bash
database_name="trader"
docker exec dtl-influxdb influx -execute "create database $database_name"
docker exec dtl-influxdb influx -execute "create retention policy \"3_day\" on $database_name duration 3d replication 1 default"