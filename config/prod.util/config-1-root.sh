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
# yum it up.
yum -y update
yum -y groupinstall 'Development Tools'
yum -y install dos2unix readline-devel zlib-devel emacs-nox mlocate freetype freetype-devel libpng libpng-devel at openssl pam_mysql fprintd-pam xslt libxml libxml-devel libxslt libxslt-devel nginx fail2ban 
yum -y install mysql mysql-server lighttpd-fastcgi php-cli php-mysql php-gd php-imap php-ldap php-odbc php-pear php-xml php-xmlrpc php-eaccelerator php-magickwand php-magpierss php-mapserver php-mbstring php-mcrypt php-mhash php-shout php-snmp php-soap php-tidy php-pear-Net-SMTP
yum -y install nagios nagios-common nagios-devel nagios-plugins-all nrpe openssl-devel xinetd
updatedb

########################################################################
# configure nginx
systemctl enable nginx.service
usermod -a -G web nginx
cp /apps/pvs/pvscore/config/prod.util/etc/nginx/nginx.conf /etc/nginx/nginx.conf
mkdir /etc/nginx/sites
cp /apps/pvs/pvscore/config/prod.util/etc/nginx/sites/*.conf /etc/nginx/sites
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.orig
# don't start until web src is installed
#systemctl start nginx.service


################################################################
## mysql
systemctl enable mysqld.service
systemctl start mysqld.service
mysqladmin -u root password $2

################################################################
## fail2ban
systemctl enable fail2ban.service
systemctl start fail2ban.service

################################################################
## atd
systemctl enable atd.service
systemctl start atd.service


########################################################################
# app dirs
sudo mkdir -p /apps
sudo chmod -R g+w /apps
sudo chown -R web:web /apps

########################################################################
# nagios
useradd nagios
echo nagios | passwd --stdin nagios
groupadd nagcmd
usermod -a -G nagcmd nagios
usermod -a -G nagcmd nginx
systemctl enable nagios.service
systemctl enable nrpe.service

echo nrpe      5666/tcp    >> /etc/services

export IP=`ifconfig eth1 | grep inet | grep -v inet6 | awk '{print $2}'`

echo server_address=$IP >> /etc/nagios/nrpe.cfg