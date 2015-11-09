#!/bin/bash
dir=`dirname $0`
cd $dir
rsync -a repos/ /etc/yum.repos.d/

yum -y clean all

yum -y install yum-cron
chkconfig yum-cron on
service yum-cron start


yum -y update

