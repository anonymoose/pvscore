#!/bin/bash

# /apps/picker/app/app/bin/exec2.sh picker pickl --st_dt 2010-01-01 --end_dt 2010-02-01 --fud derf

export ext=$1
export pkg=$2
export method=$3

cd /apps/$ext/app
source ../python/bin/activate
export PYTHONPATH=/apps/$ext/app:/apps/$ext/extensions
export LD_LIBRARY_PATH=/usr/local/lib:/usr/local/pgsql/lib:/usr/local/lib64/R/lib:$LD_LIBRARY_PATH
export PATH=$PATH:/usr/local/bin

python ../extensions/$1/bin/$2.py $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19}
#python -c "from $pkg import $method; $method()" -I ../extensions/$1/prod.ini #>> /tmp/$pkg.$method.log

cd -
