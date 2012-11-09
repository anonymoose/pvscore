#!/bin/bash

mkdir -p /apps/pvs
mkdir -p /apps/pvs/db
mkdir -p /apps/pvs/log
mkdir -p /apps/pvs/storage
chmod -R g+w /apps
chown -R web:web /apps
# exit back to kbedwell
cd /apps/pvs
rm -rf pvscore pvs
git clone git@github.com:anonymoose/pvscore.git
git clone git@github.com:anonymoose/pvs.git
export PYTHON_EGG_CACHE=/apps/pvs/.python-eggs
wget 'https://raw.github.com/pypa/virtualenv/master/virtualenv.py'
python virtualenv.py --no-site-packages .
source bin/activate
easy_install pyramid
cd pvscore
python setup.py develop
cd ../pvs
python setup.py develop
