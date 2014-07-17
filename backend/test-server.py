import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4142")
print 'a', c.tryOpen("12345")
print 'b', c.tryOpen("ABCDE")
print 'c', c.tryOpen("kalak")
