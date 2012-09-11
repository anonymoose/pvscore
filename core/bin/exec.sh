#!/bin/bash

# /apps/wm/app/app/bin/exec.sh wm wm.bin.market_latest import_splits
# /apps/wm/app/app/bin/exec.sh wm wm.bin.buyins_latest run

export ext=$1
export pkg=$2
export method=$3

export MPLCONFIGDIR=/tmp

cd /apps/$ext/app
source ../python/bin/activate
export PYTHONPATH=/apps/$ext/app:/apps/$ext/extensions
export LD_LIBRARY_PATH=/usr/local/pgsql/lib:/usr/local/lib64/R/lib:$LD_LIBRARY_PATH
export PATH=$PATH:/usr/local/bin

nice python -c "from $pkg import $method; $method($4)" -I ../extensions/$1/prod.ini >> /apps/$ext/log/$pkg.$method.log 2>&1
#python -c "from $pkg import $method; $method()" -I ../extensions/$1/prod.ini #>> /tmp/$pkg.$method.log

cd -
