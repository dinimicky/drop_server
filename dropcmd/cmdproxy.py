'''
Created on 2013-2-25

@author: ezonghu
'''
from common.multixmlstream import MultiXmlStream
from common import config
from common.state import State
from twisted.python import log
    
    
class CmdProxyServerProtocol(MultiXmlStream):   
    ActionDict = config.ActionDict
    
    def connectionMade(self):
        for k, v in CmdProxyServerProtocol.ActionDict.iteritems():
            from importlib import import_module
            m = import_module("dropcmd.cmdcallbacks")
            cmdObserver = getattr(m, k)(k, *v)
            log.msg('add Observer: %s' % k)
            self.addObserver(cmdObserver.xPathQuery, cmdObserver.checkCmdAction, 0, self)
        MultiXmlStream.connectionMade(self)

                         
from twisted.internet.protocol import ServerFactory
from twisted.internet.defer import DeferredQueue
from li.x1client import X1ClientFactory
from li.x2server import X2ServerFactory
class CmdProxyFactory(ServerFactory):
    protocol = CmdProxyServerProtocol

    def _start_x2_server(self):
        from twisted.internet import reactor
        self.x2tcp = reactor.listenTCP(config.x2InterfacePort, self.x2CliFac, 
                                       interface = config.ipAddress_LITT)
        
    def start_x1_client(self):
        from twisted.internet import reactor
        self.x1tcp = reactor.connectTCP(config.ipAddress_IAP, config.x1InterfacePort, self.x1CliFac)   
             
    def __init__(self):
        self.state = State()
        
        self.cmd_queue = DeferredQueue()
        self.x1_queue = DeferredQueue()
        self.x1CliFac = X1ClientFactory(self.cmd_queue, self.x1_queue, self.state)
        self.x1tcp = None
        
        self.x2CliFac = X2ServerFactory()
        self._start_x2_server()
