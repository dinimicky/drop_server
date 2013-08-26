'''
Created on 2013-2-25

@author: ezonghu
'''
from twisted.internet.protocol import ServerFactory
from twisted.python import log
from common.multixmlstream import MultiXmlStream
from common.multixmlstream import generateXmlFromList as toXML
from common import config
from common.state import Ping
from common.log import X2Log
from lixml import li_xml_temp
class X2ServerProtocol(MultiXmlStream):
    def __init__(self):
        self.reqMsg = None
        MultiXmlStream.__init__(self)

    def connectionMade(self):
        log.msg('x2 connection is established')
        MultiXmlStream.connectionMade(self)
        
    def onDocumentEnd(self):
        Elements = self.Elements
        if 'pingRequest' in str(Elements):
            log.msg('recv pingRequest')
            (_, Payloads) = self.check_tuple('payload', Elements)
            Payload = Payloads[0]
            log.msg('get the payload:', Payload)
            (_, Ping) = Payload[0]
            log.msg('get Ping', Ping)
            (_Result, Seq) = self.check_tuple('seqNbr', Ping)
            log.msg('get Seq:', Seq)
            Seq = int(Seq[0][0])                         

            Resp = li_xml_temp.pingX2Resp(Seq)     
            self.send(Resp)
            log.msg('send out ping resp:', Resp)
        else:#SipMessage
            log.msg('recv X2 Notify Message:', toXML(Elements))
            self.factory.x2LogHandler.msg(toXML([('LIC-Msg', Elements)]))
        MultiXmlStream.onDocumentEnd(self)
            
class X2ServerFactory(ServerFactory):
    protocol = X2ServerProtocol
    def __init__(self):
        import os.path
        Dir, Fn = os.path.split(config.x2InterfaceLog)
        self.x2LogHandler = X2Log(Fn, Dir)
        
    
        
        
