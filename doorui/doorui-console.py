#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import zmq
import zerorpc

key = raw_input('Enter access key: ');

backend = zerorpc.Client()
backend._events.setsockopt(zmq.IPV4ONLY, 0)
backend.connect("tcp://[::1]:4142")
result = backend.validate(key)

if result:
	print "Access granted for " + result
else:
	print "Access denied"

