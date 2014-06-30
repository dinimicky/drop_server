'''
Created on 2014-6-28

@author: ezonghu
'''
from twisted.words.xish import domish
from twisted.words.xish.xpath import XPathQuery
from twisted.words.xish import xmlstream
from twisted.python import log
from common.state import X1ProtocolNegotiation, X1AdmMsgs, ReqMsg
'''
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
class CmdReq(object):
    def __init__(self, action, args, **kwargs):
        self.root = domish.Element((None, 'cmd'))
        self.root.addElement('action', content = action)
        for k in args:
            self.root.addElement(k, content = kwargs[k])
            
    def toXml(self):
        return self.root.toXml()
        
class CmdResp(CmdReq):
    def __init__(self, result, comment):
        self.root = domish.Element((None, 'cmd'))
        self.root.addElement('result', content = result)
        commt = domish.Element((None, 'comment'))
        commt.addChild(comment)
        self.root.addChild(commt)
        
class CmdCB(object):
    def __init__(self, text, *args):
        self.text = text
        self.xPathQuery = XPathQuery("/action[text() = '%s']" % text)
        self.args = args

    def _getCmdRespXmlString(self, checkElement, respMsg):
        log.msg('get respMsg: %s; checkElement: %s' % (respMsg.result, checkElement))
        if respMsg.result == 'OK' and XPathQuery('//%s' %checkElement).matches(respMsg.content):
            resp = CmdResp('success', respMsg.content).toXml()
            return resp
        
        resp = CmdResp('failure', respMsg.content).toXml() 
        return resp
   
    
    def checkCmdAction(self, protoInst, element): 
        log.msg('recv cmd, action: %s, and add onetime oberser' % self.xPathQuery.queryForString(element))
        protoInst.addOnetimeObserver(xmlstream.STREAM_END_EVENT, self._sendXml2X1Client)

    def _getX1ReqXmlString(self, cmdRootElement, **kwargs):
        xmlPara = {}
        log.msg('recv cmd xml: %s' % cmdRootElement.toXml())
        for arg in self.args:
            log.msg('query arg: %s' % arg)
            xmlPara[arg] = XPathQuery("/cmd/%s" % arg).queryForString(cmdRootElement)
        
        for k, v in kwargs.iteritems():
            xmlPara[k] = v
        from importlib import import_module
        m = import_module('lixml.li_xml_temp')
        fn = getattr(m, self.text)
        return fn(**xmlPara)            
    '''
    _sendCmdRespXmlString & _sendXml2X1Client will be overlapped by inherited class
    '''    
    def _sendCmdRespXmlString(self, respMsg, protoInst):
        protoInst.send(self._getCmdRespXmlString('success', respMsg)) 

    def _sendXml2X1Client(self, protoInst):
        protoInst.factory.cmd_queue.get().addCallback(self._sendCmdRespXmlString, protoInst)
#         protoInst.factory.state.x1Seq += 1
#         protoInst.factory.x1_queue.put(self._getX1ReqXmlString(protoInst.recvRootElement, seqNbr = protoInst.factory.state.x1Seq))
#         protoInst.factory.cmd_queue.get().addCallback(self._sendCmdRespXmlString, protoInst)
        

        
class start(CmdCB):
    def _sendXml2X1Client(self, protoInst):
        log.msg('make a X1 connection')
        protoInst.factory.start_x1_client()
        log.msg('send %s ReqMsg' % X1ProtocolNegotiation.protocolProposal)
        protoInst.factory.x1_queue.put(ReqMsg(X1ProtocolNegotiation.protocolSelectionResult, 
                                              self._getX1ReqXmlString(protoInst.recvRootElement)))
        super(start, self)._sendXml2X1Client(protoInst)
        
    def _sendCmdRespXmlString(self, respMsg, protoInst):
        protoInst.send(self._getCmdRespXmlString(X1ProtocolNegotiation.protocolSelectionResult, respMsg)) 

class stop(CmdCB):
    def _sendXml2X1Client(self, protoInst):
        protoInst.factory.x1_queue.put(ReqMsg(X1AdmMsgs.endSessionAck, 
                                              self._getX1ReqXmlString(protoInst.recvRootElement)))
        super(stop, self)._sendXml2X1Client(protoInst)
        
    def _sendCmdRespXmlString(self, respMsg, protoInst):
        protoInst.send(self._getCmdRespXmlString(X1AdmMsgs.endSessionAck, respMsg))
        protoInst.factory.x1tcp.disconnect()
        
class intCfgX2(CmdCB):
    def _sendXml2X1Client(self, protoInst):
        protoInst.factory.x1_queue.put(ReqMsg(X1AdmMsgs.interfConfResponse, 
                                              self._getX1ReqXmlString(protoInst.recvRootElement)))
        super(intCfgX2, self)._sendXml2X1Client(protoInst)
        
    def _sendCmdRespXmlString(self, respMsg, protoInst):
        protoInst.send(self._getCmdRespXmlString('success', respMsg))
        
class intCfgX2X3(intCfgX2):  
    pass

class addTgtUri(CmdCB):
    def _sendXml2X1Client(self, protoInst):
        protoInst.factory.state.x1Seq += 1
        protoInst.factory.x1_queue.put(ReqMsg(X1AdmMsgs.addTargetResp, 
                                              self._getX1ReqXmlString(protoInst.recvRootElement,
                                                                      seqNbr = protoInst.factory.state.x1Seq)))
        super(addTgtUri, self)._sendXml2X1Client(protoInst)
        
class updTgtUri(CmdCB):
    def _sendXml2X1Client(self, protoInst):
        protoInst.factory.state.x1Seq += 1
        protoInst.factory.x1_queue.put(ReqMsg(X1AdmMsgs.updateTargetResp, 
                                              self._getX1ReqXmlString(protoInst.recvRootElement,
                                                                      seqNbr = protoInst.factory.state.x1Seq)))
        super(updTgtUri, self)._sendXml2X1Client(protoInst)

class remTgtUri(CmdCB):
    def _sendXml2X1Client(self, protoInst):
        protoInst.factory.state.x1Seq += 1
        protoInst.factory.x1_queue.put(ReqMsg(X1AdmMsgs.removeTargetResp, 
                                              self._getX1ReqXmlString(protoInst.recvRootElement,
                                                                      seqNbr = protoInst.factory.state.x1Seq)))
        super(remTgtUri, self)._sendXml2X1Client(protoInst)

class audTgtUri(CmdCB):
    def _sendXml2X1Client(self, protoInst):
        protoInst.factory.state.x1Seq += 1
        protoInst.factory.x1_queue.put(ReqMsg(X1AdmMsgs.auditResponse, 
                                              self._getX1ReqXmlString(protoInst.recvRootElement,
                                                                      seqNbr = protoInst.factory.state.x1Seq)))
        super(audTgtUri, self)._sendXml2X1Client(protoInst)

class audAllTgt(audTgtUri):
    pass

