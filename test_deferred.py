from twisted.internet.defer import Deferred, DeferredQueue

print """\
This example illustrates how deferreds can
be fired before they are returned. First we
make a new deferred, fire it, then add some
callbacks.
"""

# three simple callbacks

def callback_1(res):
    print 'callback_1 got', res
    return 1

def callback_2(res):
    print 'callback_2 got', res
    return 2

def callback_3(res):
    print 'callback_3 got', res
    return 3

# We create a deferred and fire it immediately:
d = Deferred()

print 'Firing empty deferred.'
d.callback(0)

# Now we add the callbacks to the deferred.
# Notice how each callback fires immediately.

print 'Adding first callback.'
d.addCallback(callback_1)

print 'Adding second callback.'
d.addCallback(callback_2)

print 'Adding third callback.'
d.addCallback(callback_3)

print"""
Because the deferred was already fired, it
invoked each callback as soon as it was added.

Now we create a deferred and fire it, but
pause it first with the pause() method.
"""

# We do the same thing, but pause the deferred:

d = Deferred()
print 'Pausing, then firing deferred.'
d.pause()
d.callback(0)

print 'Adding callbacks.'
d.addCallback(callback_1)
d.addCallback(callback_2)
d.addCallback(callback_3)

print 'Unpausing the deferred.'
d.unpause()

print "test pass result directly"
d=Deferred()
d.callback("result")
d.addBoth(callback_1)

print "test multi parameters"
def multiPara(res, a, b):
    print "res=%s;a=%s;b=%s\n" % (str(res),str(a), str(b))
    
d=Deferred()
d.addCallback(multiPara, 1,2)
d.callback("multi parameters")

print "test multi parameters & class"
class Test(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def Print(self, res, X):
        print "self=%s;res=%s;X=%s" % (str(self), str(res), str(X))
        return res
        
    @classmethod
    def classPrint(cls, res, X):
        print "class=%s;res=%s;X=%s" % (str(cls), str(res), str(X))
        
    @staticmethod
    def staticPrint(res, X):
        print "res=%s;X=%s" % (str(res), str(X))
T=Test(1,2)
d=Deferred()
d.addCallback(T.Print, X="X")
d.callback("Print")


d=Deferred()
d.addCallback(T.classPrint, X="X")
d.callback("class")
        
d=Deferred()
d.addCallback(T.staticPrint, X="X")
d.callback("static")

print "================================="
T1=Test(1,2)
T2=Test(3,4)
d=Deferred()
print d.__dict__
d.addCallback(T1.Print, "T1")
d.addCallback(T2.Print, "T2")
d.callback("Print1")
d.called=False
d.callback("Print2")
d.addCallback(T1.Print, "T1")
d.addCallback(T2.Print, "T2")


print d.__dict__

print "================================="
dq=DeferredQueue()
dq.get().addCallback(Test.classPrint, "Test1")
dq.get().addCallback(Test.classPrint, "Test2")
print dq.__dict__
dq.put("test1")
print dq.__dict__
dq.put("test2")
print dq.__dict__
dq.put("test3")
print dq.__dict__
dq.get().addCallback(Test.classPrint, "Test3")
print dq.__dict__

print dq.__dict__