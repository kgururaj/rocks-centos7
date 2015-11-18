#!/bin/bash
dir=`dirname $0`
cd $dir

if [ -f "ssh_public_keys" ]
then
  mkdir -p /root/.ssh/
  cat ssh_public_keys >> /root/.ssh/authorized_keys
fi

chown -R root:root /root
chmod u+rwX -R /root
chmod og-rwX -R /root

#Set NM_CONTROLLED=no
nw_scripts=/etc/sysconfig/network-scripts/ifcfg-*
sed -i '/NM_CONTROLLED/d' $nw_scripts
ls $nw_scripts | xargs -n 1 -I {}  bash -c 'echo NM_CONTROLLED=no >> {}'


#Copy over yum configuration
rsync -a --delete yum.repos.d/ /etc/yum.repos.d/
rsync -a yum.conf /etc/yum.conf

#proxy host and port
if [ "$#" -ge "2" ]
then
  gw_host=$1
  sed -i '/proxy/d' /etc/yum.conf
  echo "proxy=http://$gw_host:$2" >> /etc/yum.conf
fi

#Remove rocks-grub
/etc/init.d/rocks-grub stop
chkconfig rocks-grub off
chkconfig --del rocks-grub

yum -y clean all
#Nightly updates
yum -y install yum-cron
chkconfig yum-cron on
service yum-cron start
#Do an update
yum -y update

