#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
apt-get install python-pip python-dev python-virtualenv python3-pyqt5.qtquick python3-pyqt5

# Also possible on raspbian:
#apt-get install python{,3}-pifacedigitalio python{,3}-pifacecommon

