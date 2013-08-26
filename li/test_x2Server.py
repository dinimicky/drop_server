'''
Created on 2013-3-4

@author: ezonghu
'''
from twisted.trial import unittest
from common.multixmlstream import MultiXmlStream
from twisted.internet import protocol, defer
from common import config
from li import x2Server 
from twisted.python import log
pingReq = '''
<LIC-Msg>
   <lic-ModuleID>0.4.0.127.0.5.3.4.1</lic-ModuleID>
   <prot-ModuleID>0.4.0.127.0.5.3.2.1</prot-ModuleID>
   <protVersion>
      <major>1</major>
      <minor>0</minor>
   </protVersion>
   <payload>
      <ping>
         <pingType><pingRequest/></pingType>
         <seqNbr>
            47
         </seqNbr>
      </ping>
   </payload>
</LIC-Msg>
'''
x2Msg = '''
<LIC-Msg>
   <lic-ModuleID>0.4.0.127.0.5.3.4.1</lic-ModuleID>
   <prot-ModuleID>0.4.0.127.0.5.3.2.1</prot-ModuleID>
   <protVersion>
      <major>1</major>
      <minor>0</minor>
   </protVersion>
   <payload>
      <extPDU>
<IRI-Event>
   <iri-MessageSequence>
      <iMSevent>
         <iMSeventtype><sIPmessage/></iMSeventtype>
         <timeStamp>
            <generalizedTime>20130105141030.3</generalizedTime>
            <winterSummerIndication><winterTime/></winterSummerIndication>
         </timeStamp>
         <targetList>
            <TargetId-LI-IRI>
               <uri>
                  <UTF8String>sip:77777777@11.10.1.10</UTF8String>
               </uri>
            </TargetId-LI-IRI>
         </targetList>
         <correlationNumber>691C5281CF011E99314B7803359080A1</correlationNumber>
         <sIPMessage>INVITE sip:690000008001@192.168.7.70:5060;transport=UDP;user=phone;cause=302 SIP/2.0
Accept:application/sdp
Call-ID:00000000000050E6D4BD@11.10.1.10
Contact:TITAN Test User &lt;SIP:88800008@11.10.1.10:5060;transport=UDP;user=phone&gt;
Content-Length:151
Content-Type:application/sdp
CSeq:0 INVITE
From:TITAN Test User &lt;SIP:88800008@11.10.1.10:5060;transport=UDP;user=phone&gt;;tag=12345
History-Info:&lt;sip:88888888@11.10.1.10:5060;user=phone&gt;;index=1,&lt;sip:77777777@11.10.1.10:5060;cause=302?Privacy=history&gt;;index=1.1,&lt;sip:12345678@domain.com;user=phone&gt;;index=1.1.1,&lt;sip:23456789@domain2.com&gt;;index=1.1.1.1,&lt;tel:+01023456&gt;;index=1.1.1.1.1,&lt;tel:987665&gt;;index=1.1.1.1.1.1
Max-Forwards:70
To:&lt;sip:690000008001@192.168.7.70:5060;user=phone&gt;
Via:SIP/2.0/UDP 11.10.1.10:5060;branch=z9hG4bKijbrqfwraamacrz

v=0
o=TTCN_Function_Test_User 1234567890 1234567890 IN IP4 11.10.1.10
s=-
c=IN IP4 11.10.1.10
t=0 0
m=audio 5070 RTP/AVP 8
a=rtpmap:8 PCMA/8000
</sIPMessage>
         <isNonCorrelatedToCC><true/></isNonCorrelatedToCC>
         <containsCC><false/></containsCC>
      </iMSevent>
   </iri-MessageSequence>
</IRI-Event></extPDU>
   </payload>
</LIC-Msg>
'''
class LiClientProtocol(MultiXmlStream):
    def __init__(self):
        MultiXmlStream.__init__(self)
    def connectionMade(self):
        self.requests = self.factory.requests
        MultiXmlStream.connectionMade( self)
        log.msg('connection made, send request')
        self.send(self.requests.pop(0))
        if self.requests == []:
            self.factory.checkResult('OK')
            self.transport.loseConnection()
               
    def onDocumentEnd(self):
        e = self.Elements
        MultiXmlStream.onDocumentEnd(self)
        if [] != self.requests:
            log.msg('in doc end, send out request')
            self.send(self.requests.pop(0))
        else:
            self.factory.checkResult(e)
            self.transport.loseConnection()
            from twisted.internet import reactor
            reactor.stop()
        

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
    def setUp(self):
        from twisted.internet import reactor
        import sys
        log.startLogging(sys.stdout)
        self.x2Server = x2Server.X2ServerFactory()
        self.x2ServerPort = reactor.listenTCP(config.x2InterfacePort, self.x2Server, interface = config.ipAddress_LITT)

    def tearDown(self):
        x2ServerPort, self.x2ServerPort = self.x2ServerPort, None
        x2ServerPort.stopListening()


    def testPing(self):
        d = LiClient(config.ipAddress_LITT, config.x2InterfacePort, [pingReq])
        def get_resp(Keys):
            log.msg("recv key: %s" % str(Keys))
            self.assertIn('OK', str(Keys))
 
        return d.addCallback(get_resp)
 
    def testX2Msgs(self):
        d = LiClient(config.ipAddress_LITT, config.x2InterfacePort, [x2Msg])
     
        return d


