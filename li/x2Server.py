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
from common.state import Ping
from common.log import X2Log
from lixml import li_xml_temp
class X2ServerProtocol(MultiXmlStream):
    X2PingReqPath = XPathQuery('/payload/ping/pingType/pingRequest')
    getX2PingReqSeqNbr = XPathQuery('/payload/ping/seqNbr').queryForString
    X2IRIEvent = XPathQuery('/payload/extPDU/IRI-Event')
    def _genPingResp(self, element):
        SeqNbr = int(X2ServerProtocol.getX2PingReqSeqNbr(element))
        self.pingResp = li_xml_temp.pingX2Resp(SeqNbr)
        self.addOnetimeObserver(xmlstream.STREAM_END_EVENT, self._sendPingResp)
        
    def _getIRIEvent(self, element):
        if self.factory.x2LogHandler is not None:
            self.addOnetimeObserver(xmlstream.STREAM_END_EVENT, self._recordIRIEvent)
        
    def _recordIRIEvent(self):
        self.factory.x2LogHandler.msg(self.reqRootElement.toXml())
        self.reqRootElement = None
        
    def _sendPingResp(self, obj):
        print obj,self
        if self.pingResp is not None:
            self.send(self.pingResp)
            self.pingResp = None
        self.reqRootElement = None
    def __init__(self):
        self.reqRootElement = None
        self.pingResp = None
        MultiXmlStream.__init__(self)
    
    def connectionMade(self):
        log.msg('x2 connection is established')
        self.addObserver(X2ServerProtocol.X2PingReqPath, self._genPingResp)
        self.addObserver(X2ServerProtocol.X2IRIEvent, self._getIRIEvent)    
        MultiXmlStream.connectionMade(self)
        
    def onDocumentStart(self, rootElement):
        self.reqRootElement = rootElement
        MultiXmlStream.onDocumentStart(self, rootElement)
    
    def onElement(self, element):
        self.reqRootElement.addElement(element)
        MultiXmlStream.onElement(self, element)
        
        
            
class X2ServerFactory(ServerFactory):
    protocol = X2ServerProtocol
    def __init__(self):
        import os.path
        if config.x2InterfaceLog is not None:
            Dir, Fn = os.path.split(config.x2InterfaceLog)
            self.x2LogHandler = X2Log(Fn, Dir)
        else:
            self.x2LogHandler = None
        
    
        
        
