# as root
mkdir .ssh
ssh-keygen -t rsa -C "kenneth.bedwell@gmail.com"
cat ~/.ssh/id_rsa.pub
>>>> put this into github's key manager as $svr.root

vi /etc/yum.repos.d/fedora.repo 
>>> add "exclude=postgresql*" to [fedora] section

yum -y install git
mkdir -p /apps/pvs
cd /apps/pvs
git clone git@github.com:anonymoose/pvscore.git
cd ~ 
/apps/pvs/pvscore/config/prod.web/config-1-root.sh <username> <rootpw> <webpw>        <<<<---- fill in your values


su - kbedwell
cp /apps/pvs/pvscore/config/prod.common/home/.bashrc .
source .bashrc
mkdir .ssh
ssh-keygen -t rsa -C "kenneth.bedwell@gmail.com"
cat ~/.ssh/id_rsa.pub
>>>> put this into github's key manager as $svr.kbedwell
/apps/pvs/pvscore/config/prod.web/config-2-user.sh

