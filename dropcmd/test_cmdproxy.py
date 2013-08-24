'''
Created on 2013-2-28

@author: ezonghu
'''
from twisted.trial import unittest
from common.multixmlstream import MultiXmlStream
from twisted.internet import protocol, defer
from common import config
from dropcmd import cmdproxy
from twisted.python import log
class LiServerProtocol(MultiXmlStream):
    def __init__(self):
        self.counter = 1
        MultiXmlStream.__init__(self)
        
    def onDocumentEnd(self):
        if self.factory.cmds != []:
            self.send(self.factory.cmds.pop(0))
            self.counter += 1
        MultiXmlStream.onDocumentEnd(self)
    def connectionLost(self, reason):
        MultiXmlStream.connectionLost(self, reason)
        
class LiServerFactory(protocol.ServerFactory):
    protocol = LiServerProtocol
    def __init__(self, cmds = []):
        self.cmds = cmds
    

class LiClientProtocol(MultiXmlStream):
    def __init__(self):
        MultiXmlStream.__init__(self)
    def connectionMade(self):
        self.requests = self.factory.requests
        MultiXmlStream.connectionMade( self)
        self.send(self.requests.pop(0))
               
    def onDocumentEnd(self):
        e = self.Elements
        MultiXmlStream.onDocumentEnd(self)
        if [] != self.requests:
            self.send(self.requests.pop(0))
        else:
            self.factory.checkResult(e)
            self.transport.loseConnection()
        

class LiClientFactory(protocol.ClientFactory):
    protocol = LiClientProtocol
    def __init__(self, requests):
        self.requests = requests
        self.deferred = defer.Deferred()
        
    def checkResult(self, Elements):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(Elements)
           
    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            d, self.deferred = self .deferred, None
            d.errback(reason)
#            from twisted.internet import reactor
#            reactor.stop()
          
    clientConnectionLost = clientConnectionFailed

def LiClient(host, port, requests):
    factory = LiClientFactory(requests)
    from twisted.internet import reactor
    reactor.connectTCP(host, port, factory)
    return factory.deferred

class Test(unittest.TestCase):
    Requests = ['<cmd> <action>start</action></cmd> ',
                ' <cmd><action>intCfg</action> </cmd>',
                ' <cmd><action>addTgt</action> <uri>sip:123@163.com</uri><lirid>123</lirid> <ccReq>true</ccReq></cmd> ',
                ' <cmd><action>audReq</action> <uri/></cmd> ',
                ' <cmd><action>audReq</action> <uri>sip:123@163.com</uri></cmd> ',
                ' <cmd><action>updTgt</action> <uri>sip:123@163.com</uri><lirid>123</lirid> <ccReq>false</ccReq></cmd> ',
                ' <cmd><action>remTgt</action> <uri>sip:123@163.com</uri></cmd>',
                ' <cmd><action>x2Msgs</action><num>0</num></cmd>',
                ' <cmd><action>stop</action> </cmd>',
                ]

    def setUp(self):
        from twisted.internet import reactor
        import sys
        log.startLogging(sys.stdout)
        self.liServer = LiServerFactory()
        self.liServerPort = reactor.listenTCP(config.x1InterfacePort, self.liServer, interface = config.ipAddress_IAP)
        self.liProxy = cmdproxy.CmdProxyFactory()
        self.liProxyPort = reactor.listenTCP(config.cmdServerPort, self.liProxy, interface = config.ipAddress_LITT)

    def tearDown(self):
        liServerPort, self.liServerPort = self.liServerPort, None
        liServerPort.stopListening()
        self.liProxy.x2tcp.stopListening()
        liProxyPort, self.liProxyPort = self.liProxyPort, None
        liProxyPort.stopListening()
        


#    def test_start(self):
#        def createprotocolNegotiation():
#            from lixml import li_lic as lic
#            prt = lic.protocolProposal(lic.LIC_ProtocolProposal(config.LI_ADM_ObjectId, lic.ProtocolVersion(minor=0)) + 
#                                       lic.LIC_ProtocolProposal(config.LI_IRI_ObjectId, lic.ProtocolVersion(minor=0)) +
#                                       lic.LIC_ProtocolProposal(config.LI_CC_ObjectId, lic.ProtocolVersion(minor=0)))
#            return lic.LIC_Msg(config.Lic_ObjectId, config.Lic_ProtObjectId, '<protocolSelectionResult>'+prt+'</protocolSelectionResult>')
#        self.liServer.cmd = createprotocolNegotiation()
#        d = LiClient(config.ipAddress_LITT, config.cmdServerPort, Test.Requests[:2])
#        def get_resp(Keys):
#            log.msg("recv key: %s" % str(Keys))
#            for (k, v) in Keys:
#                if 'result'== k:
#                    log.msg('get result: %s:%s' % (k, v[0]))
#                    self.assertEqual("success", v[0])
#                    return
#            self.fail(Keys)
#        return d.addCallback(get_resp)
                  

    def test_all_success(self):
        import dropResp
        self.liServer.cmds = dropResp.resp
        d = LiClient(config.ipAddress_LITT, config.cmdServerPort, Test.Requests[:])
        def get_resp(Keys):
            log.msg("recv key: %s" % str(Keys))
            for (k, v) in Keys:
                if 'result'== k:
                    log.msg('get result: %s:%s' % (k, v[0]))
                    self.assertEqual("success", v[0])
                    return
            self.fail(Keys)
        return d.addCallback(get_resp)

    

