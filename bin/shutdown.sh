#!/bin/bash

APP=$1

#nothing below this line should change.

ROOT_DIR=/apps/$APP
source $ROOT_DIR/bin/activate
export PATH=$PATH:/usr/local/bin
export LD_LIBRARY_PATH=/usr/pgsql-9.1/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOT_DIR/$APP:$ROOT_DIR/pvscore
export PYTHON_EGG_CACHE=$ROOT_DIR/.python-eggs

RETVAL=0
DESC=apps.$APP
APP_PATH=$ROOT_DIR/$APP
PYTHON=$ROOT_DIR/bin/python
PASTER=$ROOT_DIR/bin/pserve
CONFIG=production.ini
USER=web
GROUP=web
LOG_FILE=$ROOT_DIR/log/$DESC.log
PID_FILE_5000=$ROOT_DIR/$DESC.5000.pid
PID_FILE_5001=$ROOT_DIR/$DESC.5001.pid

cat $PID_FILE_5000 | xargs kill
#cat $PID_FILE_5001 | xargs kill
