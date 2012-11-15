#!/bin/bash
set -x

# this should be run as root.
# config-1-root.sh kbedwell <kbedwell-pw> <web-pw>

########################################################################
# reset root password
echo $2 | passwd --stdin root

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
cp /apps/pvs/pvscore/config/prod.common/etc/ssh/sshd_config /etc/ssh/sshd_config
echo AllowUsers $1 >> /etc/ssh/sshd_config

########################################################################
# setup the firewall
/sbin/iptables -F
cp /apps/pvs/pvscore/config/prod.common/etc/iptables.up.rules /etc/iptables.up.rules
/sbin/iptables-restore < /etc/iptables.up.rules
/sbin/iptables-save > /etc/sysconfig/iptables
systemctl restart iptables.service
systemctl restart sshd.service

########################################################################
# ensure that /dev/shm is set up for parallel processing in python
# http://stackoverflow.com/questions/2009278/python-multiprocessing-permission-denied
chmod 777 /dev/shm
echo none                /dev/shm        tmpfs   rw,nosuid,nodev,noexec 0 0 >> /etc/fstab


########################################################################
# set up for postgresql-happy yumming.
curl -O http://yum.postgresql.org/9.1/fedora/fedora-17-x86_64/pgdg-fedora91-9.1-4.noarch.rpm
rpm -ivh pgdg-fedora91-9.1-4.noarch.rpm
yum -y update
yum -y groupinstall 'Development Tools'
yum -y install python-devel python-setuptools dos2unix readline-devel zlib-devel emacs-nox mlocate lapack.x86_64 lapack-devel.x86_64 atlas.x86_64 atlas.x86_64 blas.x86_64 blas-devel.x86_64 freetype freetype-devel libpng libpng-devel memcached at openssl pam_mysql fprintd-pam xslt libxml libxml-devel libxslt libxslt-devel nginx fail2ban redis postgresql91-server postgresql91-contrib postgresql91-devel python-psycopg2 nrpe nagios-plugins-all openssl-devel xinetd ntpdate
yum -y install nagios nagios-common nagios-devel nagios-plugins-all nrpe nagios-plugins-nrpe
updatedb

########################################################################
# time sync
echo 0 4 * * * root /sbin/ntpdate pool.ntp.org >> /etc/crontab
systemctl restart crond.service


########################################################################
# configure nginx
systemctl enable nginx.service
usermod -a -G web nginx
cp /apps/pvs/pvscore/config/prod.web/etc/nginx/nginx.conf /etc/nginx/nginx.conf
mkdir /etc/nginx/sites
cp /apps/pvs/pvscore/config/prod.web/etc/nginx/sites/pvs.conf /etc/nginx/sites/pvs.conf
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.orig
# don't start until web src is installed
#systemctl start nginx.service


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

################################################################
# prep for postgres
echo postgres | passwd --stdin postgres
usermod -a -G wheel postgres


################################################################
# setup the pvs service.
cp /apps/pvs/pvscore/config/prod.web/usr/lib/systemd/system/pvs.service /usr/lib/systemd/system
ln -s /usr/lib/systemd/system/pvs.service /etc/systemd/system/multi-user.target.wants/pvs.service
systemctl daemon-reload


########################################################################
# nagios
useradd nagios
echo nagios | passwd --stdin nagios
groupadd nagcmd
usermod -a -G nagcmd nagios

echo nrpe      5666/tcp    >> /etc/services

rm -rf /etc/nagios/nagios.cfg
rm -rf /etc/nagios/nrpe.cfg
rm -rf /etc/nagios/objects


cp /apps/pvs/pvscore/config/prod.common/etc/nagios/nrpe.cfg /etc/nagios
cp -R /apps/pvs/pvscore/config/prod.common/usr/lib64/nagios/plugins/* /usr/lib64/nagios/plugins

export IP=`ifconfig eth1 | grep inet | grep -v inet6 | awk '{print $2}'`
echo server_address=$IP >> /etc/nagios/nrpe.cfg

systemctl enable nrpe.service
systemctl stop nrpe.service
systemctl start nrpe.service


