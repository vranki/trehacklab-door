#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
# ZeroRPC service which can open the door with piface
# Binds to localhost port 4143
#

import time
import pifacedigitalio
import zerorpc
import zmq

class DoorDaemon(object):
    def __init__(self):
        self.pifacedigital = pifacedigitalio.PiFaceDigital()

    def openDoor(self):
        self.pifacedigital.relays[0].turn_on()
        time.sleep(1)
        self.pifacedigital.relays[0].turn_off()

s = zerorpc.Server(DoorDaemon())
s._events.setsockopt(zmq.IPV4ONLY, 0)
s.bind("tcp://[::1]:4143")
s.run()

