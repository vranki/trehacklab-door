# -*- encoding: utf-8 -*-

import zerorpc
import zmq
import sys

# Common base class for door backends

class DoorBackend(object):
    def __init__(self):
	self.door = zerorpc.Client()
    	self.door._events.setsockopt(zmq.IPV4ONLY, 0)
    	self.door.connect("tcp://[::1]:4143")

	self.bot = zerorpc.Client()
    	self.bot._events.setsockopt(zmq.IPV4ONLY, 0)
    	self.bot.connect("tcp://[::1]:4144")

# Try to open the door with key
    def tryOpen(self, key):
	result = self.validate(key)
    	if result:
		print "Opening door for " + result
   		self.door.openDoor()
		try:
			self.bot.say(result + " avasi pajan oven.")
		except:
			print "Bot not alive? Error" + sys.exc_info()[0]

    		return True

    	return False

# Must return string (username) or None
    def validate(self, key):
	pass

# Must be called if success
    def validationSuccess(self, username):
	print "Validation successful for username " + username

# Must be called if failure
    def validationFailed(self):
	print "Validation failed"

    def runServer(self):
	srv = zerorpc.Server(self)
	srv._events.setsockopt(zmq.IPV4ONLY, 0)
	srv.bind("tcp://[::1]:4142")
	srv.run()

