#!/bin/bash
database_name="trader"
docker exec dtl-influxdb influx -execute "create database $database_name"
docker exec dtl-influxdb influx -execute "create retention policy \"5_hour\" on $database_name duration 5h replication 1 default"