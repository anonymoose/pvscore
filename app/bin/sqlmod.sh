#!/bin/bash
set -x
#export sql="alter table crm_enterprise drop column logo_path2;"
#export sql="alter table core_status alter column create_dt type timestamp;"

psql -U wm -d wm -c "$1"
psql -U unittest -d unittest -c "$1"
psql -U retail -d retail -c "$1"
ssh pvs01 "psql -U wm -d wm -c '$1'"
ssh pvs02 "psql -U retail -d retail -c '$1'"

