'''
Created on 2013-2-25

@author: ezonghu
'''

'''
X2Server main function:
1. auto reply the Ping request
2. record the Notification from MGC into some log files, there is a flag to control whether to record or not.
'''
from twisted.internet.protocol import ServerFactory
from twisted.python import log
from twisted.words.xish import xmlstream   
from common.multixmlstream import MultiXmlStream
from twisted.words.xish.xpath import XPathQuery
from common import config
from common.log import X2Log
from lixml import li_xml_temp
class X2ServerProtocol(MultiXmlStream):
    X2PingReqPath = XPathQuery('/payload/ping/pingType/pingRequest')
    getX2PingReqSeqNbr = XPathQuery('/payload/ping/seqNbr').queryForString
    X2IRIEvent = XPathQuery('/payload/extPDU/IRI-Event')
    
    def _genPingResp(self, element):
        SeqNbr = int(X2ServerProtocol.getX2PingReqSeqNbr(element))
        log.msg("recv X2 Ping request, SeqNbr: %d" % SeqNbr)
        self.pingResp = li_xml_temp.pingX2Resp(SeqNbr)
        def sendPingResp(SeqNbr, x2ProtInst):
            x2ProtInst.send(x2ProtInst.pingResp)
            x2ProtInst.pingResp = None
            log.msg("send X2 Ping response, SeqNbr: %d" % SeqNbr)
        self.addOnetimeObserver(xmlstream.STREAM_END_EVENT, sendPingResp, 0, SeqNbr)
        
    def _getIRIEvent(self, element):
        log.msg('recv X2 message: %s' % X2ServerProtocol.X2IRIEvent.queryForNodes(element)[0].name)
        if self.factory.x2LogHandler is not None:
            def recordIRIEvent(x2ProtInst):
                x2ProtInst.factory.x2LogHandler.msg(x2ProtInst.reqRootElement.toXml())
            self.addOnetimeObserver(xmlstream.STREAM_END_EVENT, recordIRIEvent)
        

    def __init__(self):
        self.reqRootElement = None
        self.pingResp = None
        MultiXmlStream.__init__(self)
        self.addObserver(X2ServerProtocol.X2PingReqPath, self._genPingResp)
        self.addObserver(X2ServerProtocol.X2IRIEvent, self._getIRIEvent)    
    
    def connectionMade(self):
        log.msg('x2 connection is established')
        MultiXmlStream.connectionMade(self)
        

        
        
            
class X2ServerFactory(ServerFactory):
    protocol = X2ServerProtocol
    def __init__(self):
        import os.path
        if config.x2InterfaceLog is not None:
            Dir, Fn = os.path.split(config.x2InterfaceLog)
            self.x2LogHandler = X2Log(Fn, Dir)
        else:
            self.x2LogHandler = None
        
    
        
        
