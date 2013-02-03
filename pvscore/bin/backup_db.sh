#!/bin/bash
set -x
# backup_db.sh wm wm 
# backup_db.sh retail retail

export db=$1
export pass=$2


/usr/bin/pg_dump -U $db -O -c $pass | gzip > /apps/pvs/db/$db.sql.gz

