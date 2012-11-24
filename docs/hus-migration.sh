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
dropdb -U postgres wm
createdb -U postgres wm
psql -U postgres -c "create user wm with password 'wm';"
psql -U postgres -c 'alter database wm owner to wm;'
ssh pvs02 "pg_dump -U wm -O -c wm | gzip > production-wm.sql.gz"
scp kbedwell@pvs01:/home/kbedwell/production-wm.sql.gz .
gunzip production-wm.sql.gz
psql -U wm -d wm -f production-wm.sql
psql -U postgres -d wm -f reduce.sql
#python ../pvscore/pvscore/bin/delete_enterprise.py retail2 3
python ../pvscore/pvscore/bin/uuidkey.py wm wm /Users/kbedwell/dev/pydev/pvs/storage
#python ../pvscore/pvscore/bin/uuidkey.py wm wm /apps/pvs/storage

pg_dump -U wm -O --data-only wm > wm.sql
pg_dump -U retail -O -c retail > retail.sql

cat retail.sql | awk '/DROP CONSTRAINT/' > constraint-drops.sql
cat retail.sql | awk '/CREATE INDEX/ || /ALTER TABLE ONLY/ || /ADD CONSTRAINT/' > constraint-adds.sql
psql -U retail -d retail -f constraint-drops.sql
psql -U retail -d retail -f wm-reduced.sql
psql -U retail -d retail -f constraint-adds.sql
psql -U retail -c "update cms_site set namespace = 'ecom/whitesquares' where domain = 'healthyustore.net';"

redis-cli flushdb
sudo systemctl start pvs.service
