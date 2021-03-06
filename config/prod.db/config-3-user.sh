#!/bin/bash
sudo rm -rf /apps/pvs

sudo mkdir -p /apps/pvs/db
sudo mkdir -p /apps/pvs/log
sudo mkdir -p /apps/pvs/storage/enterprises
sudo chmod -R g+w /apps
sudo chown -R web:web /apps

cd /apps/pvs
git clone git@github.com:anonymoose/pvscore.git
sudo chown -R kbedwell.web pvscore
git clone git@github.com:anonymoose/pvs.git
sudo chown -R kbedwell.web pvs

export PYTHON_EGG_CACHE=/apps/pvs/.python-eggs
wget 'https://raw.github.com/pypa/virtualenv/master/virtualenv.py'
python virtualenv.py --no-site-packages .
source bin/activate
easy_install pyramid
pip install numpy
pip install scipy
pip install matplotlib
pip install TA-Lib


cd pvscore
python setup.py develop
cd ../pvs
python setup.py develop

