#!/bin/bash
set -x
# backup_db.sh wm wm wm wm02



export ext=$1
export db=$2
export pass=$3
export other_server=$4
export version=$5


export LD_LIBRARY_PATH=/usr/local/pgsql/$version/lib:/usr/local/lib64/R/lib:$LD_LIBRARY_PATH
export PATH=$PATH:/usr/local/bin

/usr/local/pgsql/$version/bin/pg_dump -U $db -O -c $pass | gzip > /apps/$ext/db/$ext.$db.sql.gz

/usr/bin/scp /apps/$ext/db/$ext.$db.sql.gz disco@$other_server:/apps/$ext/db
