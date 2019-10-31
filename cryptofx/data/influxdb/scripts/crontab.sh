SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

# influxdb to csv
# 30  *  *  *  * python3 /opt/deployment/cryptofx/data/influxdb/scripts/to_csv_and_s3.py
30  *  *  *  * root python3 /opt/deployment/cryptofx/data/influxdb/scripts/to_csv_and_s3.py