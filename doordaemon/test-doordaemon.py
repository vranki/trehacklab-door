#!/usr/bin/python
import zerorpc

print 'Opening door..'
c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4143")
c.openDoor()
print 'done.'


