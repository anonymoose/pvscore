# as root
mkdir .ssh
ssh-keygen -t rsa -C "kenneth.bedwell@gmail.com"
cat ~/.ssh/id_rsa.pub
>>>> put this into github's key manager as $svr.root

yum -y install git
mkdir -p /apps/pvs
cd /apps/pvs
git clone git@github.com:anonymoose/pvscore.git
cd ~ 
/apps/pvs/pvscore/config/prod.lb/config-1-root.sh <username> <rootpw> <webpw>        <<<<---- fill in your values

