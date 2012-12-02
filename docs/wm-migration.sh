#!/bin/bash
exit
#
# on db01, as kbedwell
#
# cd /apps/pvs
# rsync -avz web01-bak.eyefound.it:/apps/pvs/storage /apps/pvs
# chown -R web.web ./storage

# cd /apps/pvs/wm
# source ../bin/activate

# dropdb -U postgres retail
# createdb -U postgres retail
# psql -U postgres -c "create user retail with password 'retail';"
# psql -U postgres -c 'alter database retail owner to retail;'

# dropdb -U postgres wm
# createdb -U postgres wm
# psql -U postgres -c "create user wm with password 'wm';"
# psql -U postgres -c 'alter database wm owner to wm;'

# ssh web01-bak.eyefound.it "pg_dump -U retail -O -c retail | gzip > production-retail.sql.gz"
# scp kbedwell@web01-bak.eyefound.it:/home/kbedwell/production-retail.sql.gz .
# gunzip production-retail.sql.gz
# psql -U retail -d retail -f production-retail.sql

#
# on oldwm
#
#sudo /etc/init.d/nginx stop



#
# on db01, as kbedwell
#
# ssh oldwm "pg_dump -U wm -O -c wm | gzip > production-wm.sql.gz"
# scp kbedwell@oldwm:/home/kbedwell/production-wm.sql.gz .
# gunzip production-wm.sql.gz
# psql -U wm -d wm -f production-wm.sql


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

#
# on web01
#
sudo systemctl stop nginx


#
# on db01, as kbedwell
#
cat retail.sql | awk '/DROP CONSTRAINT/' > constraint-drops.sql
cat retail.sql | awk '/CREATE INDEX/ || /ALTER TABLE ONLY/ || /ADD CONSTRAINT/' > constraint-adds.sql
psql -U retail -d retail -f constraint-drops.sql
psql -U retail -d retail -f wm-reduced.sql
psql -U retail -d retail -f constraint-adds.sql

#
# on lb01, as root
#
# vi /etc/pound.cfg
# -- repoint wealthmakers.com to web01-bak
# systemctl restart pound.service

#
# on web01, as kbedwell
#
redis-cli flushdb

cd /apps/pvs/pvscore
git pull
cd ../pvs
git pull
cd ../wm
git pull


sudo systemctl start pvs.service
--- check that all is well on eyefound.it and healthustore.net
--- modify pvs.service and set up wm.service to take port numbers
--- install nginx wm.conf
sudo cp /pvs/pvscore/config/prod.web/etc/nginx/sites/*.conf /etc/nginx/site
sudo systemctl restart nginx
sudo systemctl start pvs.service
sudo systemctl enable wm.service
sudo systemctl start wm.service
--- check www.wealthmakers