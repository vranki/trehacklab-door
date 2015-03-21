# -*- encoding: utf-8 -*-

import zerorpc
import zmq

class DoorBackend(object):
    def __init__(self):
	self.door = zerorpc.Client()
    	self.door._events.setsockopt(zmq.IPV4ONLY, 0)
    	self.door.connect("tcp://[::1]:4143")

    def tryOpen(self, key):
    	if self.validate(key):
    		self.door.open()
    		return True

    	return False

    def validate(self, key):
	pass

    def runServer(self):
	srv = zerorpc.Server(self)
	srv._events.setsockopt(zmq.IPV4ONLY, 0)
	srv.bind("tcp://[::1]:4142")
	srv.run()

