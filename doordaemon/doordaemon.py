#!/usr/bin/python
import time
import pifacedigitalio
import zerorpc

class DoorDaemon(object):
    def __init__(self):
        self.pifacedigital = pifacedigitalio.PiFaceDigital()

    def openDoor(self):
        self.pifacedigital.relays[0].turn_on()
        time.sleep(1)
        self.pifacedigital.relays[0].turn_off()

s = zerorpc.Server(DoorDaemon())
s.bind("tcp://127.0.0.1:4143")
s.run()

