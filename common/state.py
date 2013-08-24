'''
Created on 2013-2-27

@author: ezonghu
'''
class State(object):
    def __init__(self):
        self.action = None
        self.x1TcpConn = TcpConn.disconnected
        self.x2TcpConn = TcpConn.disconnected
        self.x1ProtocolNegotiation = None
        self.x1AdmMsgs = []
        self.x1Ping = None
        self.x2Ping = None
        self.x2IriMsgs = []
        self.x1Seq = 0
        self.x2Seq = 0
        

'''
class Msg is used to transfer information between cmdserver and X1/X2
'''
class Msg(object):
    def __init__(self, msgtype = None, content = None):
        self.type = msgtype
        self.content = content
        
class ReqMsg(Msg):
    def __init__(self, expectedRes, content):
        self.expectedRes = expectedRes
        super(ReqMsg, self).__init__(msgtype = "cmd", content = content)

class RespMsg(Msg):
    def __init__(self, result = None, content = None):
        self.result = result
        super(RespMsg, self).__init__(msgtype = "cmd", content = content)

class TcpMsg(Msg):
    def __init__(self, result = None, content = None):
        self.result = result
        super(TcpMsg, self).__init__(msgtype = "tcp", content = content)        
        
        
class TcpConn(object):
    connecting = "connecting"
    connected = "connected"
    disconnected = "disconnected"
    disconnecting = "disconnecting"
    
class X1ProtocolNegotiation(object):
    protocolProposal = "protocolProposal"
    protocolSelectionResult = "protocolSelectionResult"
    
class X1AdmMsgs(object):
    interfConfRequest = 'interfConfRequest'
    interfConfResponse = 'interfConfResponse'
    endSessionRequest = 'endSessionRequest'
    endSessionAck = 'endSessionAck'
    addTargetRequest = 'addTargetRequest'
    addTargetResp = 'addTargetResp'
    removeTargetRequest = 'removeTargetRequest'
    removeTargetResp = 'removeTargetResp'
    updateTargetRequest = 'updateTargetRequest'
    updateTargetResp = 'updateTargetResp'
    auditRequest = 'auditRequest'
    auditResponse = 'auditResponse'
    alarmNotification = 'alarmNotification'
    
class Ping(object):
    timeout = 'timeout'

class X2IriMsgs(object):
    iMSevent = 'iMSevent'
        
        

        
        
        

