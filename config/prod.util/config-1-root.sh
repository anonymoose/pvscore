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
cp /apps/pvs/pvscore/config/prod.util/etc/iptables.up.rules /etc/iptables.up.rules
/sbin/iptables-restore < /etc/iptables.up.rules
/sbin/iptables-save > /etc/sysconfig/iptables
systemctl restart iptables.service
systemctl restart sshd.service

########################################################################
# yum it up.
yum -y update
yum -y groupinstall 'Development Tools'
yum -y install nagios nagios-common nagios-devel nagios-plugins-nrpe nagios-plugins-all nrpe openssl-devel xinetd gcc glibc glibc-common gd gd-devel  dos2unix readline-devel zlib-devel emacs-nox mlocate at openssl xslt libxml libxml-devel libxslt libxslt-devel fail2ban
yum -y install httpd php lighttpd-fastcgi php-cli php-mysql php-gd php-imap php-ldap php-odbc php-pear php-xml php-xmlrpc php-eaccelerator php-magickwand php-magpierss php-mapserver php-mbstring php-mcrypt php-mhash php-shout php-snmp php-soap php-tidy php-pear-Net-SMTP freetype freetype-devel libpng libpng-devel pam_mysql fprintd-pam
yum -y install mysql mysql-server
updatedb

########################################################################
# time sync
echo '0 4 * * * root /sbin/ntpdate pool.ntp.org' >> /etc/crontab
systemctl restart crond.service

########################################################################
# configure apache
systemctl enable httpd.service


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
usermod -a -G root nagios
chmod g+r /var/log/messages
htpasswd -b /etc/nagios/passwd nagiosadmin $2

echo nrpe      5666/tcp    >> /etc/services


rm -rf /etc/nagios/nagios.cfg
rm -rf /etc/nagios/nrpe.cfg
rm -rf /etc/nagios/objects/*.cfg

cp /apps/pvs/pvscore/config/prod.util/etc/nagios/nagios.cfg /etc/nagios
cp /apps/pvs/pvscore/config/prod.common/etc/nagios/nrpe.cfg /etc/nagios
cp /apps/pvs/pvscore/config/prod.util/etc/nagios/objects/*.cfg /etc/nagios/objects
cp -R /apps/pvs/pvscore/config/prod.common/usr/lib64/nagios/plugins/* /usr/lib64/nagios/plugins

export IP=`ifconfig eth1 | grep inet | grep -v inet6 | awk '{print $2}'`
echo server_address=$IP >> /etc/nagios/nrpe.cfg

systemctl enable nagios.service
systemctl enable nrpe.service
systemctl stop nagios.service
systemctl start nagios.service
systemctl stop nrpe.service
systemctl start nrpe.service

cp /apps/pvs/pvscore/config/prod.util/etc/httpd/conf.d/nagios-vhost.conf /etc/httpd/conf.d
usermod -a -G web apache
systemctl start httpd.service

