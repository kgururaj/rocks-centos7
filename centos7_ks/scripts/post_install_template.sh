#!/bin/bash

if [ -f "ssh_public_keys" ]
then
  mkdir -p /root/.ssh/
  cat ssh_public_keys >> /root/.ssh/authorized_keys
fi

chown -R root:root /root
chmod -R u+rwX /root
chmod -R og-rwX /root

#Set NM_CONTROLLED=no
nw_scripts=/etc/sysconfig/network-scripts/ifcfg-*
sed -i '/NM_CONTROLLED/d' $nw_scripts
ls $nw_scripts | xargs -n 1 -I {}  bash -c 'echo NM_CONTROLLED=no >> {}'

#Should be the last line in this script
curl -k "https://Kickstart_PrivateKickstartHost/Kickstart_PrivateKickstartBasedir/sbin/public/setPxeboot.cgi?action=os"

