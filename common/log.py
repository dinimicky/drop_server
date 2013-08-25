'''
Created on 2013-8-24

@author: Brilliant
'''

from twisted.python.logfile import LogFile
class X2Log(object):
    def __init__(self, logHandler):
        self.logHandler = logHandler
        self.Counter = 1
        
    def msg(self, content=""):
        head = "=="*10+"START"+"=="*10
        tail = "=="*10+"=END="+"=="*10
        self.logHandler.write("\n%d:%s\n" % (self.Counter, head))
        for line in content.split('\n'):
            if line != "":
                self.logHandler.write("%d:%s\n" % (self.Counter, line))
        self.logHandler.write("%d:%s\n" % (self.Counter, tail))
        self.Counter += 1
        self.logHandler.flush()
        
        

if __name__ == "__main__":
    fd = open("test.log", "w")
    test = X2Log(fd)
    test.msg("test1\ntest2\n")
    test.msg("test3\ntest4\n")  
    fd.close()  