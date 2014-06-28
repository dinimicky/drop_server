'''
Created on 2013-2-25

@author: ezonghu

Note: without receiving response, the whole process will exit.
'''
from twisted.internet.protocol import ClientFactory
from twisted.internet import task, reactor
from twisted.python import log
from twisted.words.xish import xmlstream
from twisted.words.xish.xpath import XPathQuery

from common.multixmlstream import MultiXmlStream
from common.state import TcpConn, RespMsg, TcpMsg
from common import config
from lixml import li_xml_temp


class X1ClientProtocol(MultiXmlStream):
    X1PingRespPath = XPathQuery('/payload/ping/pingType/pingResponse')
    getX1PingRespSeqNbr = XPathQuery('/payload/ping/seqNbr').queryForString
    X1AlarmPath = XPathQuery('/payload/extPDU/LI-ADM-Event/lI-ADM-MessageSequence/alarmNotification')
    callLater = reactor.callLater
    timeOut = 30

    def connectionMade(self):
        log.msg('x1 tcp connection is made')
        self.alarmCounter = 0
        self.factory.x1_queue.get().addCallback(self.cmdReceived)
        if config.pingEnable:
            self.lcping = task.LoopingCall(self._sendPingRequest)
            self.lcping.start(config.ping_delay)
        MultiXmlStream.connectionMade(self)
        def recordX1Alarm(element):
            self.alarmCounter += 1
            log.msg("recv X1 total alrams: %d" % self.alarmCounter)
            log.msg("recv X1 alarm: %s" % element.toXml())
        self.addObserver(X1ClientProtocol.X1AlarmPath, recordX1Alarm)
          
    def cmdReceived(self, reqMsg):
        if reqMsg.type == 'cmd':
            log.msg("recv cmd: %s" % reqMsg.content)
            self.reqMsg = reqMsg
            self._sendX1Xml(self.reqMsg.content)

        self.factory.x1_queue.get().addCallback(self.cmdReceived)

    def connectionLost(self, Why):
        log.msg("connnect is lost, reason:%s" % Why)
        
        if hasattr(self, 'lcping') and self.lcping is not None:
            lcping, self.lcping = self.lcping, None
            lcping.stop()
        log.msg('server existed')
        reactor.stop()
        if self.factory.x1_queue:
            self.factory.x1_queue = None
        return Why

    def _sendPingRequest(self):
        self.factory.state.x1Seq += 1                         
        self.send(li_xml_temp.pingX1Req(self.factory.state.x1Seq))
        log.msg("x1 ping request is sent out, x1Seq =", self.factory.state.x1Seq)

        def recvPingResp(cancelPingId, x1Seq, element):
            cancelPingId.cancel()
            RecvX1Seq = int(X1ClientProtocol.getX1PingRespSeqNbr(element))
            log.msg("recv x1 ping response, x1Seq=%d; send out x1Seq=%d" % (RecvX1Seq, x1Seq))
            
        def ping_cancel():
            self.removeObserver(X1ClientProtocol.X1PingRespPath, recvPingResp)
            log.msg("x1 ping response is not received ")
            self.transport.loseConnection()
            
        pingCallID = self.callLater(config.ping_timeout, ping_cancel)
        self.addOnetimeObserver(X1ClientProtocol.X1PingRespPath, recvPingResp, 0, pingCallID, self.factory.state.x1Seq)

        
    def _sendX1Xml(self, xml):
        log.msg('x1 send out xml directly')
        self.send(xml)
        expectResp = XPathQuery("//%s" % (self.reqMsg.expectedRes))
        def recvCmdResp(cancelCmdCallID, element):
            cancelCmdCallID.cancel()
            def send_resp2cmd_queue(x1CliInst):
                log.msg('recv X1 response')
                x1CliInst.factory.cmd_queue.put(RespMsg(result="OK", content=x1CliInst.recvRootElement))
            self.addOnetimeObserver(xmlstream.STREAM_END_EVENT, send_resp2cmd_queue)
            
        
        def cancelCmdResp():
            self.removeObserver(expectResp, recvCmdResp)
            log.msg("X1 did't receive response. request:%s." % self.reqMsg.content)
            self.factory.cmd_queue.put(RespMsg(result="Unavailable", content=None))
            self.reqMsg = None
            self.transport.loseConnection()
            
        cancelCmdRespCallId = self.callLater(X1ClientProtocol.timeOut, cancelCmdResp)
        self.addOnetimeObserver(expectResp, 
                                recvCmdResp, 0, cancelCmdRespCallId)
        
        return cancelCmdResp
      
class X1ClientFactory(ClientFactory):
    protocol = X1ClientProtocol
    def __init__(self, cmd_queue, x1_queue, state):
        self.cmd_queue = cmd_queue
        self.x1_queue = x1_queue
        self.state = state
