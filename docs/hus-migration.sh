#!/bin/bash
set -x
# on pvs03
# from apps/pvs/pvs

# dropdb -U postgres retail2
# createdb -U postgres retail2
# dropdb -U postgres retail
# createdb -U postgres retail
# psql -U retail -d retail -f ../backup/pvs03-retail.sql 
# psql -U retail2 -d retail2 -f ../backup/pvs02-retail.sql 

sudo systemctl stop pvs.service
pg_dump -U retail -O -c retail > /tmp/production-retail-`date +"%Y-%m-%d-%I-%M-%S"`.sql
dropdb -U postgres retail2
createdb -U postgres retail2
psql -U postgres -c "create user retail2 with password 'retail2';"
psql -U postgres -c 'alter database retail2 owner to retail2;'
ssh pvs02 "pg_dump -U retail -O -c retail > production-retail.sql"
scp kbedwell@pvs02:/home/kbedwell/production-retail.sql .
psql -U retail2 -d retail2 -f production-retail.sql
rm production-retail.sql
python ../pvscore/pvscore/bin/delete_enterprise.py retail2 3
#python ../pvscore/pvscore/bin/uuidkey.py retail2 retail2 /Users/kbedwell/dev/pydev/pvs/storage
python ../pvscore/pvscore/bin/uuidkey.py retail2 retail2 /apps/pvs/storage

pg_dump -U retail2 -O --data-only retail2 > retail2.sql
pg_dump -U retail -O -c retail > retail.sql
cat retail.sql | awk '/DROP CONSTRAINT/' > constraint-drops.sql
cat retail.sql | awk '/CREATE INDEX/ || /ALTER TABLE ONLY/ || /ADD CONSTRAINT/' > constraint-adds.sql
psql -U retail -d retail -f constraint-drops.sql
psql -U retail -d retail -f retail2.sql
psql -U retail -d retail -f constraint-adds.sql
psql -U retail -c "update cms_site set namespace = 'ecom/whitesquares' where domain = 'healthyustore.net';"

redis-cli flushdb
sudo systemctl start pvs.service
