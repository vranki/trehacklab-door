#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import zmq
import zerorpc

key = raw_input('Enter access key: ');

backend = zerorpc.Client()
backend._events.setsockopt(zmq.IPV4ONLY, 0)
backend.connect("tcp://[::1]:4142")

if backend.validate(key):
	print "Access granted"
else:
	print "Access denied"

