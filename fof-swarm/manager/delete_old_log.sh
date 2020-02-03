#!/bin/bash
find /data/fof_current/log -type f -mtime +30 -exec rm -f {} \;