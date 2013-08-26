'''
Created on 2013-8-24

@author: Brilliant
'''

from twisted.python.logfile import LogFile
class X2Log(LogFile):
    def __init__(self, name, directory):
        self.Counter = 1
        LogFile.__init__(self, name, directory, maxRotatedFiles=10)
    def msg(self, content=""):
        head = "=="*10+"START"+"=="*10
        tail = "=="*10+"=END="+"=="*10
        LogFile.write(self, "\n%d:%s\n" % (self.Counter, head))
        for line in content.split('\n'):
            if line != "":
                LogFile.write(self, "%d:%s\n" % (self.Counter, line))
        LogFile.write(self, "%d:%s\n" % (self.Counter, tail))
        self.Counter += 1
#         LogFile.flush(self)
        
        

if __name__ == "__main__":
    import os.path
    Dir, fn = os.path.split("./test.log")
    test = X2Log(fn, Dir)
    test.msg("test1\ntest2\n")
    test.msg("test3\ntest4\n")   
