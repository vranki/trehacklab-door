import sys
import os
import zerorpc

if len(sys.argv) < 2:
	print "Usage: %s [passcodes.txt]" % sys.argv[0]
	sys.exit()

passcode_file = sys.argv[1]

class TreDoorRPC(object):
    door = zerorpc.Client()
    door.connect("tcp://127.0.0.1:4143")

    def tryOpen(self, key):

    	if self.validate(key):
    		self.door.open()

    		return True

    	return False

    def validate(self, key):
    	key = key.lower()

    	for line in file(passcode_file):
    		line = line.strip().lower()

    		if key == line:
    			return True

    	return False

if __name__ == '__main__':
	srv = zerorpc.Server(TreDoorRPC())
	srv.bind("tcp://0.0.0.0:4142")
	srv.run()