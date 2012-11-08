#!/bin/bash

# /apps/pvs/pvscore/pvscore/bin/exec.sh pvs pvs.bin.eye_process process_upload

export ext=$1
export pkg=$2
export method=$3

export MPLCONFIGDIR=/tmp

cd /apps/$ext/$ext
source ../bin/activate
export PYTHONPATH=/apps/$ext/$ext:/apps/$ext/pvscore
export LD_LIBRARY_PATH=/usr/local/pgsql/lib:/usr/local/lib64/R/lib:$LD_LIBRARY_PATH
export PATH=$PATH:/usr/local/bin

nice python -c "from $pkg import $method; $method($4)" -I production.ini >> /apps/$ext/log/$pkg.$method.log 2>&1
#python -c "from $pkg import $method; $method()" -I ../extensions/$1/prod.ini #>> /tmp/$pkg.$method.log

cd -