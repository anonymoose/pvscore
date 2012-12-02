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
cp /apps/pvs/pvscore/config/prod.lb/etc/iptables.up.rules /etc/iptables.up.rules
/sbin/iptables-restore < /etc/iptables.up.rules
/sbin/iptables-save > /etc/sysconfig/iptables
systemctl restart iptables.service
systemctl restart sshd.service

########################################################################
# yum it up.
yum -y update
yum -y groupinstall 'Development Tools'
yum -y install Pound nagios nagios-common nagios-devel nagios-plugins-nrpe nagios-plugins-all nrpe openssl-devel xinetd httpd php mysql gcc glibc glibc-common dos2unix readline-devel zlib-devel emacs-nox mlocate at openssl xslt libxml libxml-devel libxslt libxslt-devel fail2ban 
updatedb

########################################################################
# time sync
echo '0 4 * * * root /sbin/ntpdate pool.ntp.org' >> /etc/crontab
systemctl restart crond.service

################################################################
## fail2ban
systemctl enable fail2ban.service
systemctl start fail2ban.service

################################################################
## atd
systemctl enable atd.service
systemctl start atd.service

########################################################################
# pound
systemctl enable pound.service
rm -f /etc/pound.cfg
cp /apps/pvs/pvscore/config/prod.lb/etc/pound.cfg /etc
cp /apps/pvs/pvscore/config/prod.lb/etc/pki/tls/certs/*.pem /etc/pki/tls/certs
systemctl start pound.service


########################################################################
# nagios
useradd nagios
echo nagios | passwd --stdin nagios
groupadd nagcmd
usermod -a -G nagcmd nagios
usermod -a -G root nagios
chmod g+r /var/log/messages

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


