'''
Created on 2013-8-27

@author: ezonghu
'''
from twisted.internet import task
from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.python import log
from li.x1client import X1ClientFactory, X1ClientTimeoutError, X1PingTimeoutError
from twisted.internet.defer import DeferredQueue
from common.state import State, TcpConn, ReqMsg, X1ProtocolNegotiation
from lixml import li_xml_temp
from common import config
import sys
log.startLogging(sys.stdout)

class X1ClientTest(unittest.TestCase):


    def setUp(self):
        self.tr = proto_helpers.StringTransport()
        self.clock = task.Clock()
        cmd_queue = DeferredQueue()
        x1_queue = DeferredQueue()
        state = State()
        factory = X1ClientFactory(cmd_queue, x1_queue, state)
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        config.pingEnable = False 
        
        


#     def tearDown(self):
#         pass
    
#     def _test(self, cmd, expected):
#         pass
    def _cmdReceived(self, Res):
        return Res
    
    def check_result(self, result, expected):
        self.assertEqual(result.result, expected)
        
    def test_connection(self):
        self.proto.makeConnection(self.tr)
        log.msg(self.proto.factory.cmd_queue.__dict__)
        d = self.proto.factory.cmd_queue.get().addCallback(self._cmdReceived)
        d.addCallback(self.check_result, TcpConn.connected)
        log.msg(self.proto.factory.cmd_queue.__dict__)
        return d
        
    def test_start(self):
        self.test_connection()

        Start = ReqMsg(expectedRes = X1ProtocolNegotiation.protocolSelectionResult, content = li_xml_temp.start())
        self.proto.factory.x1_queue.put(Start)
        self.assertIn(X1ProtocolNegotiation.protocolProposal, self.tr.value())
        self.tr.clear()
        self.proto.dataReceived(li_xml_temp.Start_Resp)
        d = self.proto.factory.cmd_queue.get().addCallback(self._cmdReceived)
        log.msg(self.proto.factory.cmd_queue.__dict__)
        d.addCallback(self.check_result, 'OK')
        return d
    
    def test_a_ping(self):
        self.test_connection()
        self.proto.sendPingRequest()
        self.assertIn("pingRequest", self.tr.value())
        self.tr.clear()
        (d, _pingCallID) = self.proto.pingResult[0]
        self.proto.dataReceived(li_xml_temp.X1_Ping_Resp)
        return self.assertIn('pingResponse', d.result)
        
    def test_start_timeout(self):
        self.proto.timeOut = 1
        self.test_connection()
        Start = ReqMsg(expectedRes = X1ProtocolNegotiation.protocolSelectionResult, content = li_xml_temp.start())
        self.proto.factory.x1_queue.put(Start)
        (d, _callID) = self.proto.result[0]
        self.assertIn(X1ProtocolNegotiation.protocolProposal, self.tr.value())
        self.tr.clear()
        self.clock.advance(self.proto.timeOut)
        return self.assertFailure(d, X1ClientTimeoutError)
        
    def test_ping_timeout(self):
        config.ping_delay=1
        config.ping_timeout=2
        config.pingEnable = True
        self.test_connection()
        self.assertIn("pingRequest", self.tr.value())
        (d, _pingCallID) = self.proto.pingResult[0]
        self.tr.clear()
        self.clock.advance(config.ping_timeout)
        return self.assertFailure(d, X1PingTimeoutError)


