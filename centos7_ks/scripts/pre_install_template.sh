#!/bin/bash

cpus=`grep processor /proc/cpuinfo |sort|uniq|wc -l`
arch=`uname -m`
curl -k "https://Kickstart_PrivateKickstartHost/Kickstart_PrivateKickstartBasedir/sbin/kickstart.cgi?arch=${arch}&np=${cpus}"
python disk.py --force_format compute #compute node, don't really care

