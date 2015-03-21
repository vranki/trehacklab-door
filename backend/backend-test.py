#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import zerorpc
import zmq

backend = zerorpc.Client()
backend._events.setsockopt(zmq.IPV4ONLY, 0)
backend.connect("tcp://[::1]:4142")

print 'a', backend.tryOpen("123456")
print 'b', backend.tryOpen("ABCDEF")
print 'c', backend.tryOpen("")

