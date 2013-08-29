'''
Created on 2013-2-25

@author: ezonghu
'''
from common.multixmlstream import MultiXmlStream
from twisted.words.xish import xmlstream
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
    def __init__(self):
        self.Elements = []
        MultiXmlStream.__init__(self)   
    def connectionMade(self):
        log.msg("generate a connection, self is " + str(self))
        self.cmd_queue = self.factory.cmd_queue
        self.x1_queue = self.factory.x1_queue
        self.state = self.factory.state
        self.x1CliFac = self.factory.x1CliFac
        self.x1tcp = self.factory.x1tcp
        self.cmd_queue.get().addCallback(self.x1RespReceived)
        MultiXmlStream.connectionMade(self)
    
    def onDocumentStart(self, rootElement):
        if 'cmd' == rootElement.name:
            MultiXmlStream.onDocumentStart(self, rootElement)
        else:
            
            self.dispatch(self , xmlstream.STREAM_ERROR_EVENT)
            self.transport.loseConnection()     
            
    def onDocumentEnd(self):
        Elements = self.Elements
        (Bool, Action) = self.check_cmd(Elements)
       
        if not Bool:
            self.send_cmd_resp("failure", str(Elements))

        else:
            self.do(Action, Elements)
        MultiXmlStream.onDocumentEnd(self)       

    def connectionLost(self, reason):
        MultiXmlStream.connectionLost(self, reason)
        
    def do(self, Action, Elements):
        log.msg('get Elements %s, Action is %s' % (Elements, Action))
        self.state.action = Action
        Func = getattr(self, '_do_%s' % Action, None)
        
        if Func is None:
            self.state.action = None
            log.msg("can't get function _do_%s." % Action)
            return None
        try:
            return Func(Elements)
        except Exception, e:
            log.msg('when execute %s meet error: %s' % (Func, e))
            return None
    def done(self, Action, RespMsg):
        log.msg('get RespMsg %s, Action is %s' % (RespMsg, Action))
        Func = getattr(self, '_done_%s' % Action, None)
        
        if Func is None:
            self.state.action = None
            log.msg("can't get function _done_%s." % Action)
            return None
        try:
            Func(RespMsg)
            log.msg("try to close the connection")
            self.transport.loseConnection()
        except:
            return None

    def _start_x1_connection(self):
        from twisted.internet import reactor
        self.factory.x1tcp = reactor.connectTCP(config.ipAddress_IAP, config.x1InterfacePort, self.x1CliFac)
                
    def _do_start(self, Elements):
        if self.state.x1TcpConn == TcpConn.disconnected:
            self.state.x1TcpConn = TcpConn.connecting
            self.cmd_queue.get().addCallback(self.x1RespReceived)
            self._start_x1_connection()
            self.x1_queue.put(ReqMsg(expectedRes = X1ProtocolNegotiation.protocolSelectionResult, content = li_xml_temp.start()))
        else:
            log.msg("%s: wrong tcp status: %s" % (self, self.state.x1TcpConn))
            Response = self.send_cmd_resp("failure", "wrong tcp status: %s" % self.state.x1TcpConn)
            self.send(Response) 
    def _done_start(self, respMsg):
        Str = str(respMsg.content)
        if respMsg.result == 'Unexpected':
            return
        
        self.state.action = None
        if respMsg.result == "Unavailable":
            log.msg("X1 did't receive response.")
            Resp = self.send_cmd_resp('failure', "X1 did't receive response.")
            
            return 
        
        if ('noApplicableProtocolAvailable' in Str) or ('noCompatibleVersionSupported' in Str):
            log.msg("X1 lic negotiation failed, the Elements: %s" % Str)
            Resp = self.send_cmd_resp('failure', Str)
            
            return
        if 'protocolSelectionResult' in Str:
            log.msg('X1 lic negotiation success, the Elements: %s' % Str)
            Resp = self.send_cmd_resp('success', Str)
            log.msg('generate Resp %s' % Resp)
            
    def _do_stop(self, Elements): #send endSessionRequest
        if self.state.x1TcpConn == TcpConn.connected:
            self.state.x1TcpConn = TcpConn.disconnecting
            self.x1_queue.put(ReqMsg(expectedRes = X1AdmMsgs.endSessionAck, content = li_xml_temp.stop()))
        else:
            log.msg("%s: wrong tcp status: %s" % (self, self.state.x1TcpConn))
            Response = self.send_cmd_resp("failure", "wrong tcp status: %s" % self.state.x1TcpConn)
            self.send(Response) 
    def _done_stop(self, respMsg): #recv endSessionRequest
        log.msg('recv from x1 client:', str(respMsg.content))
        if respMsg.result == 'Unexpected':
            return
        
        self.state.action = None
        if respMsg.result == "Unavailable":
            log.msg("X1 did't receive response.")
            self.send_cmd_resp('failure', "X1 did't receive response.")
            
            return 

        self.state.x1TcpConn = TcpConn.disconnected
        self.factory.x1tcp.disconnect()
        log.msg('x1 has been disconnected.')
        self.send(self.send_cmd_resp('success', 'tcp has been disconnected.'))             
    def __proceed_cmdRequest(self, expectedResult, x1ReqXml):
        if self.state.x1TcpConn == TcpConn.connected:
            self.x1_queue.put(ReqMsg(expectedRes = expectedResult, content = x1ReqXml))
        else:
            self.state.action = None
            log.msg("%s: wrong tcp status: %s" % (self, self.state.x1TcpConn))
            Response = self.send_cmd_resp("failure", "wrong tcp status: %s" % self.state.x1TcpConn)
            self.send(Response)           
    def _do_intCfgX2X3(self, Elements):   
        self.__proceed_cmdRequest(expectedResult = X1AdmMsgs.interfConfResponse, x1ReqXml = li_xml_temp.intCfgX2X3())   
    def _do_intCfgX2(self, Elements):   
        self.__proceed_cmdRequest(expectedResult = X1AdmMsgs.interfConfResponse, x1ReqXml = li_xml_temp.intCfgX2())   
    def __proceed_x1Response(self, respMsg):
        Str = str(respMsg.content)
        log.msg('recv from x1 client:', Str)
        if respMsg.result == 'Unexpected':
            return
        
        Action, self.state.action = self.state.action, None
        if respMsg.result == "Unavailable":
            log.msg("X1 did't receive response. Current Action:", Action)
            Resp = self.send_cmd_resp('failure', "X1 did't receive response.")
            
            
            return 
        #check interfConf success or not
        if 'success' in Str:
            log.msg('X1 %s success, the Elements: %s' % (Action, Str))
            Resp = self.send_cmd_resp('success', Str)
        else:#meet error
            log.msg('X1 %s failed, the Elements: %s' % (Action,Str))
            Resp = self.send_cmd_resp('failure', Str)
        log.msg("self is " + str(self))   
        log.msg('generate Resp %s' % Resp)
        self.transport.write(Resp)        
    def _done_intCfgX2(self, respMsg):
        self.__proceed_x1Response(respMsg)
    def _done_intCfgX2X3(self, respMsg):
        self.__proceed_x1Response(respMsg)   
    def __storetgt2dict(self, Elements):
        d = {}
        for k, v in Elements:
            if k == 'uri':
                if v == []:
                    d[k] = None
                else:
                    d[k] = v[0]
            elif k == 'lirid':
                d[k] = v[0]
            elif k == 'ccReq':
                d[k] = v[0]
            elif k == 'num':
                d[k] = int(v[0])

        return d
    def _do_addTgt(self, Elements):
        d = self.__storetgt2dict(Elements)
        uri = d['uri']
        ccReq = True if d['ccReq'] == 'True' else False
        lirid = int(d['lirid'])
        self.state.x1Seq += 1    
        self.__proceed_cmdRequest(expectedResult=X1AdmMsgs.addTargetResp, 
                                  x1ReqXml = li_xml_temp.addTgtUri(self.state.x1Seq, uri, lirid, ccReq))
    def _done_addTgt(self, respMsg):
        self.__proceed_x1Response(respMsg)
    def _do_remTgt(self, Elements):
        d = self.__storetgt2dict(Elements)
        uri = d['uri']
        self.state.x1Seq += 1       
        self.__proceed_cmdRequest(expectedResult=X1AdmMsgs.removeTargetResp, 
                                  x1ReqXml = li_xml_temp.remTgtUri(self.state.x1Seq, uri))
    def _done_remTgt(self, respMsg):
        self.__proceed_x1Response(respMsg)
    def _do_updTgt(self, Elements):
        d = self.__storetgt2dict(Elements)
        uri = d['uri']
        ccReq = True if d['ccReq'] == 'True' else False
        lirid = int(d['lirid'])
        self.state.x1Seq += 1
        self.__proceed_cmdRequest(expectedResult=X1AdmMsgs.updateTargetResp, 
                                  x1ReqXml = li_xml_temp.updTgtUri(self.state.x1Seq, uri, lirid, ccReq))
    def _done_updTgt(self, respMsg):
        self.__proceed_x1Response(respMsg)
    def _do_audReq(self, Elements):
        d = self.__storetgt2dict(Elements)
        uri = d['uri']
        self.state.x1Seq += 1
        AudReq = li_xml_temp.audTgtUri(self.state.x1Seq, uri)
        self.__proceed_cmdRequest(expectedResult=X1AdmMsgs.auditResponse, x1ReqXml = AudReq)
    def _done_audReq(self, respMsg):
        self.__proceed_x1Response(respMsg)
    def _do_audAll(self, Elements):
        self.state.x1Seq += 1
        AudReq = li_xml_temp.audAllTgt(self.state.x1Seq)
        self.__proceed_cmdRequest(expectedResult=X1AdmMsgs.auditResponse, x1ReqXml = AudReq)
    def _done_audAll(self, respMsg):
        self.__proceed_x1Response(respMsg)     
    def x1RespReceived(self, respMsg=RespMsg()):
        if respMsg.type == 'tcp':
            log.msg('X1 recv tcp status: ', respMsg.result)
            self.state.x1TcpConn = respMsg.result
        elif respMsg.type == 'cmd':
            self.done(self.state.action, respMsg)
#         self.cmd_queue.get().addCallback(self.x1RespReceived)
    def check_cmd(self, Elements):
        (Result, Values) = self.check_tuple('action', Elements)
        if Result == False:
            return (False, None)
        if len(Values) != 1:
            return (False, None)
        Action=Values[0][0]
        if Action not in CmdProxyServerProtocol.ActionDict:
            return (False, None)
        Options = CmdProxyServerProtocol.ActionDict[Action]
        if (len(Options)+ 1) != len(Elements):
            return (False, None)
        for Opt in Options:
            (Result, Values) = self.check_tuple(Opt, Elements)
            if Result == False:
                return (False, None)
        return (True, Action)
    def send_cmd_resp(self, result= 'success', comment=""):
        from common.multixmlstream import generateXml as xml
        Resp = xml('cmd', [('result',result), ('comment', comment)])
        self.send(Resp)
#         self.transport.loseConnection()
        return
                         
from twisted.internet.protocol import ServerFactory
from twisted.internet.defer import DeferredQueue
from li.x1client import X1ClientFactory
from li.x2Server import X2ServerFactory
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
