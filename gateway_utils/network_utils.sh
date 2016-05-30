#!/bin/bash

function fix_rocks_eth
{
    local filename="/etc/udev/rules.d/70-persistent-net.rules"
    sed -i '/eth0/d' $filename
    sed -i '/eth1/d' $filename
    sed -i 's/eth2/eth0/g' $filename
    sed -i 's/eth3/eth1/g' $filename
}

function create_bridge
{
  if [ "$#" -lt "3" ];
  then
    echo "Needs 3 arguments : <eth> <bridge> <onboot> [<ip> <netmask>] "
    return;
  fi
  local eth="$1";
  local br="$2";
  local onboot="$3";
  local ip="";
  local netmask="";
  local bootproto="dhcp"
  if [ "$#" -ge "5" ]
  then
    ip="$4";
    netmask="$5";
    bootproto="none";
  fi
  ifcfg_file="/etc/sysconfig/network-scripts/ifcfg-$eth"
  if [ -f  "$ifcfg_file" ]
  then
    sed -i -e '/ONBOOT/d' -e '/BOOTPROTO/d' -e '/NM_CONTROLLED/d' -e '/PEERDNS/d' -e '/BRIDGE/d' -e '/DEFROUTE/d' "$ifcfg_file"
  else
    echo "DEVICE=$eth" > $ifcfg_file
  fi
  echo "
ONBOOT=yes
BOOTPROTO=none
NM_CONTROLLED=no
PEERDNS=no
BRIDGE=$br
" >> "$ifcfg_file"

  echo "
DEVICE=$br
TYPE=Bridge
STP=on
DELAY=0
ONBOOT=$onboot
BOOTPROTO=$bootproto
MTU=1500
NM_CONTROLLED=no
PEERDNS=no
IPV6INIT=no
" > /etc/sysconfig/network-scripts/ifcfg-$br
  if [ "$ip" != "" ]
  then
    echo "
IPADDR=$ip
NETMASK=$netmask
" >> /etc/sysconfig/network-scripts/ifcfg-$br
  fi
  echo "In a Rocks cluster, run: 'rocks set host interface options <hostname> iface=$eth options=\"noreport\"' to avoid configuration files being over-written"
  #/bin/cp -f /etc/sysconfig/network-scripts/ifcfg-$br /etc/sysconfig/network-scripts/ifcfg-$br-local
}

function create_vlan
{
  if [ "$#" -lt "3" ];
  then
    echo "Needs 3 arguments : <eth> <vlan_id> <onboot> [<ip> <netmask>] "
    return;
  fi
  local eth="$1";
  local vlan="$2";
  local onboot="$3";
  local ip="";
  local netmask="";
  local bootproto="dhcp"
  if [ "$#" -ge "5" ]
  then
    ip="$4";
    netmask="$5";
    bootproto="none";
  fi
  echo "
VLAN=yes
DEVICE=${eth}.${vlan}
BOOTPROTO=$bootproto
ONBOOT=$onboot
NM_CONTROLLED=no
PEERDNS=no
IPV6INIT=no
" > /etc/sysconfig/network-scripts/ifcfg-${eth}.${vlan}
  if [ "$ip" != "" -a  "$ip" != "none" ]
  then
    echo "
IPADDR=$ip
NETMASK=$netmask
DEFROUTE=no
" >> /etc/sysconfig/network-scripts/ifcfg-${eth}.${vlan}
  fi
}

function create_bridge_on_vlan
{
  if [ "$#" -lt "4" ];
  then
    echo "Needs 3 arguments : <eth> <bridge> <vlan_id> <onboot> [<ip> <netmask>] "
    return;
  fi
  local eth="$1";
  local br="$2";
  local vlan="$3";
  local onboot="$4";
  local ip="";
  local netmask="";
  local bootproto="dhcp"
  if [ "$#" -ge "6" ]
  then
    ip="$5";
    netmask="$6";
    bootproto="none";
  fi
  create_vlan $eth $vlan $onboot "none" "none"
  create_bridge $eth.$vlan $br $onboot $ip $netmask 
}
