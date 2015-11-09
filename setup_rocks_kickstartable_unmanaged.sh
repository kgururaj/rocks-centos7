#!/bin/bash

if [ "$#" -lt "1" ]
then
  echo "Needs <list_of_appliances>"
  exit -1
fi

for val in "$@"
do
  rocks remove appliance "$val"
  rocks add appliance "$val" membership="$val" node=compute
  rocks set appliance attr "$val" kickstartable True
  rocks set appliance attr "$val" managed False
done
