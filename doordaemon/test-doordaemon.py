#!/usr/bin/python
import zerorpc
import zmq

print 'Opening door..'
c = zerorpc.Client()
c._events.setsockopt(zmq.IPV4ONLY, 0)
c.connect("tcp://[::1]:4143")
c.openDoor()
print 'done.'


