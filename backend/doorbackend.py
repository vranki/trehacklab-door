# -*- encoding: utf-8 -*-

import zerorpc
import zmq


# Common base class for door backends

class DoorBackend(object):
    def __init__(self):
	self.door = zerorpc.Client()
    	self.door._events.setsockopt(zmq.IPV4ONLY, 0)
    	self.door.connect("tcp://[::1]:4143")

# Try to open the door with key
    def tryOpen(self, key):
	result = self.validate(key)
    	if result:
		print "Opening door for " + result
   		self.door.open()
    		return True

    	return False

# Must return string (username) or None
    def validate(self, key):
	pass

# Must be called if success
    def valicationSuccess(self, username):
	print "Validation successful for username " + username

# Must be called if failure
    def valicationFailed(self):
	print "Validation failed"

    def runServer(self):
	srv = zerorpc.Server(self)
	srv._events.setsockopt(zmq.IPV4ONLY, 0)
	srv.bind("tcp://[::1]:4142")
	srv.run()

