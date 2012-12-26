#!/bin/bash
sudo rm -rf /apps/pvs

sudo mkdir -p /apps/pvs/db
sudo mkdir -p /apps/pvs/log
sudo mkdir -p /apps/pvs/storage
sudo chmod -R g+w /apps
sudo chown -R web:web /apps

cd /apps/pvs
git clone git@github.com:anonymoose/pvscore.git
sudo chown -R kbedwell.web pvscore
git clone git@github.com:anonymoose/pvs.git
sudo chown -R kbedwell.web pvs
git clone git@github.com:anonymoose/wm.git
sudo chown -R kbedwell.web wm
git clone git@github.com:anonymoose/stats.git
sudo chown -R kbedwell.web stats
export PYTHON_EGG_CACHE=/apps/pvs/.python-eggs
wget 'https://raw.github.com/pypa/virtualenv/master/virtualenv.py'
python virtualenv.py --no-site-packages .
source bin/activate
easy_install pyramid

cd pvscore
python setup.py develop
cd ../pvs
python setup.py develop
cd ../wm
python setup.py develop

########################################################################
# numpy/scipy
pip install numpy
pip install scipy
pip install matplotlib


########################################################################
# nfs
su -c "echo db01-bak.eyefound.it:/apps/pvs/storage /apps/pvs/storage  nfs   rw,noatime    0   0 >> /etc/fstab"
sudo mount db01-bak.eyefound.it:/apps/pvs/storage /apps/pvs/storage

sudo systemctl start nginx.service
sudo systemctl enable pvs.service
sudo systemctl start pvs.service
sudo systemctl enable wm.service
sudo systemctl start wm.service
sudo systemctl start htttpd

