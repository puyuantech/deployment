#!/bin/bash
database_name="trader"
docker exec dtl-influxdb influx -execute "create database $database_name"
docker exec dtl-influxdb influx -execute "create retention policy \"1_hour\" on $database_name duration 1h replication 1 default"