'''
Created on 2013-2-25

@author: ezonghu
'''
from twisted.internet.protocol import ClientFactory
from twisted.internet import task, reactor, defer
from twisted.python import log
from common.multixmlstream import MultiXmlStream
from common.state import TcpConn, Ping, RespMsg, TcpMsg
from common import config
from lixml import li_xml_temp

class X1ClientTimeoutError(Exception):
    pass
class X1ClientProtocol(MultiXmlStream):
    callLater = reactor.callLater
    timeOut = 30
    
    def __init__(self):
        self.result = []
        self.reqMsg = None
        self.pingReq = 0
        self.pingResp = 0
        MultiXmlStream.__init__(self)

    def connectionMade(self):
        log.msg('x1 tcp connection is made')
        self.x1_queue = self.factory.x1_queue
        self.state = self.factory.state
        self.cmd_queue = self.factory.cmd_queue
        self.cmd_queue.put(TcpMsg(TcpConn.connected))
        self.x1_queue.get().addCallback(self.cmdReceived)
        if config.pingEnable:
            self.lcping = task.LoopingCall(self.sendPingRequest)
            self.lcping.start(config.ping_delay, False)


        MultiXmlStream.connectionMade(self)
        
    def sendPingRequest(self):
        self.pingReq +=1
        if (self.pingReq - self.pingResp) >= (config.ping_timeout / config.ping_delay):
            self.state.x1Ping = Ping.timeout
            log.msg('x1 ping timeout happens, PingReq: %d; PingResp: %d.' % self.pingReq, self.pingResp)
        self.state.x1Seq += 1                          
        self.send(li_xml_temp.pingX1Req(self.state.x1Seq))
    
    def _cancel(self, d):
        log.msg("X1 did't receive response. request:%s." % self.reqMsg.content)
        self.reqMsg = None
        self.cmd_queue.put(RespMsg(result="Unavailable", content=None))
        d.errback(X1ClientTimeoutError())
        
    def _sendX1Xml(self, xml):
        d = defer.Deferred()
        callID = self.callLater(self.timeOut, self._cancel, d)
        self.result.append((d, callID))
        log.msg('x1 send out xml:', xml)
        self.send(xml)
        return d
    def cmdReceived(self, reqMsg):
        if reqMsg.type == 'cmd':
            log.msg("recv cmd: %s" % reqMsg.content)
            self.reqMsg = reqMsg
            self._sendX1Xml(self.reqMsg.content)

        self.x1_queue.get().addCallback(self.cmdReceived)
    def onDocumentEnd(self):
        Elements = self.Elements

        if self.reqMsg is not None and self.reqMsg.expectedRes in str(Elements):
            self.reqMsg = None
            d, callID = self.result.pop(0)
            callID.cancel()
            d.callback(str(Elements))
            log.msg('recv response: %s' % Elements)
            self.factory.cmd_queue.put(RespMsg(result="OK", content=Elements))
        elif 'ping' in str(Elements):
            self.pingResp += 1            
        else:
            log.msg("recv unexpected message:%s" % str(Elements))
#            self.factory.cmd_queue.put(RespMsg(result="Unexpected", content=Elements))
        MultiXmlStream.onDocumentEnd(self)
    def connectionLost(self, Why):
        if self.x1_queue:
            self.x1_queue = None
class X1ClientFactory(ClientFactory):
    protocol = X1ClientProtocol
    def __init__(self, cmd_queue, x1_queue, state):
        self.cmd_queue = cmd_queue
        self.x1_queue = x1_queue
        self.state = state

        
        
