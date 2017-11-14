#!/bin/bash

if [ "$#" -ne "2" ]
then
  echo "Two args <rmm_hostname/IP> <ipmi_passwd_file>"
  exit -1
fi

rmm_hostname="$1"
ipmi_passwd_file="$2"

for channel in {1..3}
do
  ipmitool -f ${ipmi_passwd_file} -U root -I lanplus -H ${rmm_hostname} sol set enabled true $channel
  for user in {1..3}  #root is generally in the first 3 users
  do
    ipmitool -f ${ipmi_passwd_file} -U root -I lanplus -H ${rmm_hostname} sol payload enable $channel $user
  done
done
