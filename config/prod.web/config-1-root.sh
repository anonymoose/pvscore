#!/bin/bash
set -x

# this should be run as root.
# config-1-root.sh kbedwell <kbedwell-pw> <web-pw>

########################################################################
# reset root password
echo $2 | passwd --stdin

########################################################################
# add an admin user.  kbedwell to start.  Add him to the wheel group
adduser web
echo $3 | passwd --stdin web
usermod -a -G wheel web
adduser $1
echo $2 | passwd --stdin $1
usermod -a -G wheel $1
usermod -a -G web $1

########################################################################
# standard ssh setup
cp /apps/pvs/pvscore/config/prod.web/etc/ssh/sshd_config /etc/ssh/sshd_config
echo AllowUsers $1 >> /etc/ssh/sshd_config

########################################################################
# setup the firewall
/sbin/iptables -F
cp /apps/pvs/pvscore/config/prod.web/etc/iptables.up.rules /etc/iptables.up.rules
/sbin/iptables-restore < /etc/iptables.up.rules
/sbin/iptables-save > /etc/sysconfig/iptables
systemctl restart iptables.service
systemctl restart sshd.service

########################################################################
# ensure that /dev/shm is set up for parallel processing in python
# http://stackoverflow.com/questions/2009278/python-multiprocessing-permission-denied
chmod 777 /dev/shm
echo none                /dev/shm        tmpfs   rw,nosuid,nodev,noexec 0 0 >> /etc/fstab

# fix the linker for postgres and R libraries
#curl 'http://wwww.palmvalleysoftware.com/download/ld.so.conf' >> /etc/ld.so.conf
#/sbin/ldconfig

########################################################################
# set up for postgresql-happy yumming.
curl -O http://yum.postgresql.org/9.1/fedora/fedora-17-x86_64/pgdg-fedora91-9.1-4.noarch.rpm
rpm -ivh pgdg-fedora91-9.1-4.noarch.rpm
yum -y update
yum -y groupinstall 'Development Tools'
yum -y install python-devel python-setuptools dos2unix readline-devel zlib-devel emacs-nox mlocate lapack.x86_64 lapack-devel.x86_64 atlas.x86_64 atlas.x86_64 blas.x86_64 blas-devel.x86_64 freetype freetype-devel libpng libpng-devel memcached at openssl pam_mysql fprintd-pam xslt libxml libxml-devel libxslt libxslt-devel nginx fail2ban redis postgresql91-server postgresql91-contrib postgresql91-devel python-psycopg2
updatedb

########################################################################
# configure nginx
systemctl enable nginx.service
usermod -a -G web nginx
cp /apps/pvs/pvscore/config/prod.web/etc/nginx/nginx.conf /etc/nginx/nginx.conf
mkdir /etc/nginx/sites
cp /apps/pvs/pvscore/config/prod.web/etc/nginx/sites/pvs.conf /etc/nginx/sites/pvs.conf
systemctl start nginx.service

################################################################
## fail2ban
systemctl enable fail2ban.service
systemctl start fail2ban.service

################################################################
## atd
systemctl enable atd.service
systemctl start atd.service

################################################################
## Redis
systemctl enable redis.service
systemctl start redis.service

################################################################
## Logrotate
#cp /apps/pvs/pvscore/config/prod.web/etc/logrotate.d/apps /etc/logrotate.d/apps
#systemctl enable logrotate.service
#systemctl start logrotate.service


