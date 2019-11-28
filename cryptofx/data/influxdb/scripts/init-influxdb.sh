#!/bin/bash
database_name="trader"
docker exec dtl-influxdb influx -execute "create database $database_name"
docker exec dtl-influxdb influx -execute "create retention policy \"2_day\" on $database_name duration 2d replication 1 default"