#!/bin/bash

#Disable selinux
yum -y install libselinux-utils
setenforce 0
sed -i -e '/SELINUX\s*=\s*enforcing/c\
SELINUX=disabled' -e '/SELINUX\s*=\s*permissive/c\
SELINUX=disabled' /etc/selinux/config

#Disable NetworkManager
chkconfig NetworkManager off
service NetworkManager stop

#ssh directory
mkdir -p /root/.ssh
chown -R root:root /root/.ssh
chmod og-rwX -R /root/.ssh

#Virtualization tools
yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum -y clean all
yum -y install virt-install virt-manager ansible-lint ansible iptables-services facter xorg-x11-xauth ipmitool

#Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward
echo "Add 'net.ipv4.ip_forward = 1' in /etc/sysctl.conf"

#Use IPTables instead of firewalld
chkconfig firewalld off
service firewalld stop
chkconfig iptables on

echo "On multi-network nodes/VMs, ensure:
DEFROUTE=no
PEERDNS=no
IPV6INIT=no
NM_CONTROLLED=no
ONBOOT=yes"

