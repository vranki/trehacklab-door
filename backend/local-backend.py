#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
import sys
import os
import zerorpc
import zmq

from doorbackend import DoorBackend

if len(sys.argv) < 2:
	print "Usage: %s [passcodes.txt]" % sys.argv[0]
	sys.exit()

passcode_file = sys.argv[1]

class DoorBackendLocal(DoorBackend):
    def __init__(self):
	DoorBackend.__init__(self)

    def validate(self, key):
    	key = key.lower()

    	for line in file(passcode_file):
    		line = line.strip().lower()

    		if key == line:
    			return True

    	return False

if __name__ == '__main__':
	server = DoorBackendLocal()
	server.runServer()

