#!/bin/bash
set -x
# on pvs03
# from apps/pvs/pvs
pg_dump -U retail -O -c retail > /tmp/production-retail-`date +"%Y-%m-%d-%I-%M-%S"`.sql
createuser -U postgres -S -D -R -e retail2
dropdb -U postgres retail2
createdb -U postgres retail2
ssh pvs02 "pg_dump -U retail -O -c retail > production-retail.sql"
scp kbedwell@pvs02:/home/kbedwell/production-retail.sql .
psql -U postgres -c 'alter database retail2 owner to retail2;'
psql -U retail2 -d retail2 -f production-retail.sql
rm production-retail.sql
python ../pvscore/pvscore/bin/delete_enterprise.py retail2 3
python ../pvscore/pvscore/bin/uuidkey.py retail2 retail2 /Users/kbedwell/dev/pydev/pvs/storage

