'''
Created on 2013-2-25

@author: ezonghu
'''
from twisted.internet.protocol import ServerFactory
from twisted.python import log
from common.multixmlstream import MultiXmlStream
from common.state import Ping, RespMsg

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
            log.msg('recv X2 Notify Message:', str(Elements))
            self.factory.messages.append(Elements)
        MultiXmlStream.onDocumentEnd(self)
            
class X2ServerFactory(ServerFactory):
    protocol = X2ServerProtocol
        
    
        
        
