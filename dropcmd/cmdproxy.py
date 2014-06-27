'''
Created on 2013-2-25

@author: ezonghu
'''
from common.multixmlstream import MultiXmlStream
from twisted.words.xish import xmlstream
from twisted.words.xish.xpath import XPathQuery
from common import config
from common.state import State, TcpConn, ReqMsg, RespMsg, X1ProtocolNegotiation, X1AdmMsgs
from lixml import li_xml_temp
from twisted.python import log

'''
drop_server
===========
dropServer has 3 port 
Port 1 is to accept the command xml stream by TCP
Port 2 is to send some xml stream to SUT according to the command by TCP
Port 3 is to receive some xml stream from SUT by TCP, the xml streams will be write to some file.

dropClient
==========
dropClient 
1. send the command xml stream to dropServer accroding to the input parameters
2. receive the result (success/failure) of the command from dropServer


What kind of command is specified?
 ========================================
 Request:
 ========================================
 Start:
 <cmd>
     <action>start</action>
 </cmd>

 Stop:
 <cmd>
     <action>stop</action>
 </cmd>

intChgX2:
<cmd>
    <action>intChg</action>
    <x2IP>127.0.0.1</x2IP>
    <x2Port>11111<x2Port> 
</cmd>

intChgX2X3:
<cmd>
    <action>intChg</action>
    <x2IP>127.0.0.1</x2IP>
    <x2Port>11111<x2Port>
    <x3IP>127.0.0.1</x3IP>
    <x3Port>22222<x3Port>    
</cmd>


audReq:
<cmd>
    <action>audReq</action> 
    <uri>sip:123@163.com</uri>
</cmd>

audAll:
<cmd>
    <action>audAll</action> 
</cmd>
addTarget:
<cmd>
    <action>addTgt</action>
    <uri>sip:123@163.com</uri>
    <ccReq>True</ccReq>
    <lirid>1234</lirid>
</cmd>


 removeTarget:
 <cmd>
     <action>remTgt</action>
     <uri>sip:123@163.com</uri>
 </cmd>
 
 updateTarget:
 <cmd>
     <action>updTgt</action>
     <uri>sip:123@163.com</uri>
     <ccReq>true</ccReq>
     <lirid>1234</lirid>
 </cmd>
 
 ========================================
 Response:
 ========================================
 <cmd>
     <result>success/failure</result>
 </cmd>   
'''
class CmdCB(object):
    def __init__(self, text, protoInst = None):
        self.xPathQuery = XPathQuery("/action[text() = '%s']" % text)
    
    def sendXml2X1Client(self, protoInst):
        rootElement = protoInst.reqRootElement
    
    def Observer(self, protoInst, element): 
        protoInst.addOnetimeObserver(xmlstream.STREAM_END_EVENT, self.send2x1_queue)
    
    
class CmdProxyServerProtocol(MultiXmlStream):   
    ActionDict = {'start' : [],
                  'stop' : [],
                  'intCfgX2' : [],
                  'intCfgX2X3' : [],
                  'audReq' : ['uri'],
                  'audAll' : [],
                  'addTgt' : ['uri', 'ccReq', 'lirid'],
                  'remTgt' : ['uri'],
                  'updTgt' : ['uri', 'ccReq', 'lirid']}
    
    def connectionMade(self):
        for k in CmdProxyServerProtocol.ActionDict:
            cmdObserver = CmdCB(k, self)
            self.addObserver(cmdObserver.xPathQuery, cmdObserver.Observer, 0, self)
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
    def __init__(self):
        self.state = State()
        
        self.cmd_queue = DeferredQueue()
        self.x1_queue = DeferredQueue()
        self.x1CliFac = X1ClientFactory(self.cmd_queue, self.x1_queue, self.state)
        self.x1tcp = None
        
        self.x2CliFac = X2ServerFactory()
        self._start_x2_server()
