#!/bin/bash
set -x
# on db01, as kbedwell

cd /apps/pvs/wm
source ../bin/activate

dropdb -U postgres retail
createdb -U postgres retail
psql -U postgres -c "create user retail with password 'retail';"
psql -U postgres -c 'alter database retail owner to retail;'

dropdb -U postgres wm
createdb -U postgres wm
psql -U postgres -c "create user wm with password 'wm';"
psql -U postgres -c 'alter database wm owner to wm;'

ssh web01-bak.eyefound.it "pg_dump -U retail -O -c retail | gzip > production-retail.sql.gz"
scp kbedwell@web01-bak.eyefound.it:/home/kbedwell/production-retail.sql.gz .
gunzip production-retail.sql.gz
psql -U retail -d retail -f production-retail.sql

ssh oldwm "pg_dump -U wm -O -c wm | gzip > production-wm.sql.gz"
scp kbedwell@oldwm:/home/kbedwell/production-wm.sql.gz .
gunzip production-wm.sql.gz
psql -U wm -d wm -f production-wm.sql




psql -U postgres -d wm -f ../pvscore/docs/wm-reduce.sql
#python ../pvscore/pvscore/bin/delete_enterprise.py retail2 3
#python ../pvscore/pvscore/bin/uuidkey.py wm wm /Users/kbedwell/dev/pydev/pvs/storage
python ../pvscore/pvscore/bin/uuidkey.py wm wm /apps/pvs/storage

update wm_portfolio from wm-keys.log
    alter table wm_portfolio add column customer_id_uuid uuid;
    update wm_portfolio set customer_id_uuid = '585aa316-faad-4a2f-9037-bd6db271b408' where customer_id = 272696;
    ::::
    alter table wm_portfolio drop column customer_id;
    alter table wm_portfolio rename column customer_id_uuid to customer_id;

pg_dump -U wm -O --data-only wm > wm-reduced.sql
pg_dump -U retail -O -c retail > retail.sql

cat retail.sql | awk '/DROP CONSTRAINT/' > constraint-drops.sql
cat retail.sql | awk '/CREATE INDEX/ || /ALTER TABLE ONLY/ || /ADD CONSTRAINT/' > constraint-adds.sql
psql -U retail -d retail -f constraint-drops.sql
psql -U retail -d retail -f wm-reduced.sql
psql -U retail -d retail -f constraint-adds.sql

redis-cli flushdb
sudo systemctl start pvs.service

