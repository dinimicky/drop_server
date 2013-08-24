class Foo(object):
    pass

def f1(self, value):
    print "f1 ", value
    
Foo.f2=f1

Foo().f2(1)

import types
Foo.newF = types.MethodType(f1, None, Foo)
print Foo.newF
print Foo.f2
print Foo().newF(1)
print Foo().f2(1)

import new
Foo.newI = new.instancemethod(f1, None, Foo)
print Foo().newI(1)

@staticmethod
def staticf(value):
    print "staticf", value
    
Foo.f3=staticf
print Foo.f3(2)

print "my foo instance"
foo=Foo()
print foo.f2(1)
print foo.newF(1)
print foo.f3(2)

print "======================="
class A(object):
    def __init__(self):
        l = locals()
        print l
        print l.pop("self")
        print l
        print locals()
        self.a="I am a"
    def get(self):
        print self.__class__
        
class B(A):
    def __init__(self):
        self.b="I am b"
        super(B, self).__init__(self)
    def getName(self):
        print "I am B"
        
a=A()
a.get()

print A.get
print a.get

def remote_call(Str):
    return Str
def remove_call(self, Str="Default"):
    return Str
new_class = type('Cat', (object,), {'meow': remote_call('meow'),
                                    'eat': remote_call('eat'),
                                    'sleep': remove_call})

print new_class()
print new_class().eat
print new_class().sleep
print new_class().sleep()
print new_class().sleep('abcd')

class MyObj(object):
    def __attributesFromDict__(self, Dict):
        print Dict.pop("self")
        print self
        for k, v in Dict.items():
            setattr(self, k, v)
            
class N1(MyObj):
    def __init__(self, A=1, B=2, C=3):
        print locals()
        self.__attributesFromDict__(locals())
        print self.__dict__
        
n1=N1()
print n1.A
print n1.B
print n1.C

class MyObj2(object):
    def __init__(self, **Dict):
        print self
        for k, v in Dict.items():
            setattr(self, k, v)
            
class N2(MyObj2):
    pass

n2=N2(A=1,B=2,C=3)
print n2.__dict__
print n2.A
print n2.B
print n2.C

