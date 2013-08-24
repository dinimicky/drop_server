from twisted.internet import protocol, defer
from twisted.trial import unittest
from multixmlstream import MultiXmlStream

class LiServerProtocol(MultiXmlStream):
    Response = '<cmd><result>success</result><comment>%s</comment></cmd>'
    def __init__(self):
        self.counter = 1
        MultiXmlStream.__init__(self)
        
    def onDocumentEnd(self):
        self.send(LiServerProtocol.Response % str(self.counter))
        self.counter += 1
        MultiXmlStream.onDocumentEnd(self)

class LiServerFactory(protocol.ServerFactory):
    protocol = LiServerProtocol
    

class LiClientProtocol(MultiXmlStream):
    def __init__(self):
        self.Requests = ['<cmd> <action>start</action></cmd> ',
                         ' <cmd><action>stop</action> </cmd>',
                         ' <cmd><action>addTgt</action> <uri>sip:123@163.com</uri><lirid>123</lirid> <ccReq>true</ccReq></cmd> ',
                         ' <cmd><action>updTgt</action> <uri>sip:123@163.com</uri><lirid>123</lirid> <ccReq>false</ccReq></cmd> ',
                         ' <cmd><action>remTgt</action> <uri>sip:123@163.com</uri></cmd>'
                         ]
        MultiXmlStream.__init__(self)
    def connectionMade(self):
        MultiXmlStream.connectionMade( self)
        self.send(self.Requests.pop(0))
               
    def onDocumentEnd(self):
        e = self.Elements
        MultiXmlStream.onDocumentEnd(self)
        if [] != self.Requests:
            self.send(self.Requests.pop(0))
        else:
            self.factory.checkResult(e)
            self.transport.loseConnection()
        

class LiClientFactory(protocol.ClientFactory):
    protocol = LiClientProtocol
    def __init__(self, cmd):
        self.cmd = cmd
        self.deferred = defer.Deferred()
        
    def checkResult(self, Elements):
        if self.deferred is not None:
            d, self.deferred = self .deferred, None
            d.callback(Elements)
           
    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            d, self.deferred = self .deferred, None
            d.errback(reason)
#            from twisted.internet import reactor
#            reactor.stop()
          
    clientConnectionLost = clientConnectionFailed

def LiClient(host, port, cmd):
    factory = LiClientFactory(cmd)
    from twisted.internet import reactor
    reactor.connectTCP(host, port, factory)
    return factory.deferred

class LiServerProtocolTest(unittest.TestCase):
    testXml={'start': '<cmd> <action>start</action></cmd> ',
             'stop':' <cmd><action>stop</action> </cmd>',
             'addTgt':' <cmd><action>addTgt</action> <uri>sip:123@163.com</uri><lirid>123</lirid> <ccReq>true</ccReq></cmd> ',
             'updTgt':' <cmd><action>updTgt</action> <uri>sip:123@163.com</uri><lirid>123</lirid> <ccReq>false</ccReq></cmd> ',
             'remTgt':' <cmd><action>remTgt</action> <uri>sip:123@163.com</uri></cmd>',
             }
    def setUp(self):
        from twisted.internet import reactor
        liFactory = LiServerFactory()
        self.LiPort = reactor.listenTCP(0, liFactory, interface = '127.0.0.1')
        self.LiPortnum = self.LiPort.getHost().port
       
    def tearDown(self):
        LiPort, self.LiPort = self.LiPort, None
        return LiPort.stopListening()

    def cmd_verify(self,cmd, ExpertResult):
        d = LiClient( '127.0.0.1', self.LiPortnum, cmd)
        def get_resp(Keys):
            for (k, v) in Keys:
                if 'result'== k:
                    return self.assertEqual(ExpertResult, v[0])
            self.fail(Keys)
        d.addCallback(get_resp)
        return d
    def cmd_success(self, cmd):
        return self.cmd_verify(cmd, "success")
       
    def cmd_failure(self, cmd):
        return self.cmd_verify(cmd, 'failure')
           
    def test_start(self):
        return self.cmd_success(self.testXml['start'])

