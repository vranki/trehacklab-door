#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
apt-get install python-pip
pip install zerorpc
pip install pifacedigitalio
# Also on raspbian:
#apt-get install python3-pifacedigitalio

