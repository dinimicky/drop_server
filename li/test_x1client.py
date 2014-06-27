'''
Created on 2013-8-27

@author: ezonghu
'''
from twisted.internet import task
from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.python import log
from li.x1client import X1ClientFactory
from twisted.internet.defer import DeferredQueue
from common.state import State, TcpMsg, ReqMsg, RespMsg, X1ProtocolNegotiation
from lixml import li_xml_temp
from common import config
import sys
log.startLogging(sys.stdout)

class X1ClientTest(unittest.TestCase):


    def setUp(self):
        self.tr = proto_helpers.StringTransportWithDisconnection()
        self.clock = task.Clock()
        cmd_queue = DeferredQueue()
        x1_queue = DeferredQueue()
        state = State()
        factory = X1ClientFactory(cmd_queue, x1_queue, state)
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.proto.callLater = self.clock.callLater
        self.tr.protocol = self.proto
        config.pingEnable = False 
        self.cmd_data = []

    def getCmdData(self, data):
        self.cmd_data.append(data)           
            
    def test_connection(self):
        self.proto.makeConnection(self.tr)
        self.assertEqual(1, len(self.proto.cmd_queue.pending))
        self.assertEqual(1, len(self.proto.x1_queue.waiting))
        self.cmd_data = []
        self.proto.cmd_queue.get().addCallback(self.getCmdData)
        self.assertIsInstance(self.cmd_data[0], TcpMsg)
            
        
        
    def test_start(self):
        self.proto.makeConnection(self.tr)
        self.proto.cmd_queue.get().addCallback(self.getCmdData)
        reqCmd = ReqMsg(X1ProtocolNegotiation.protocolSelectionResult, li_xml_temp.start())
        self.proto.x1_queue.put(reqCmd)
        self.assertIn(X1ProtocolNegotiation.protocolProposal, self.tr.value())
        self.tr.clear()
        self.proto.dataReceived(li_xml_temp.Start_Resp)
        self.proto.cmd_queue.get().addCallback(self.getCmdData)
        self.assertIsInstance(self.cmd_data[1], RespMsg)
        self.assertEqual("OK", self.cmd_data[1].result)
        
    def test_start_timeout(self):
        self.proto.makeConnection(self.tr)
        self.proto.cmd_queue.get().addCallback(self.getCmdData)
        reqCmd = ReqMsg(X1ProtocolNegotiation.protocolSelectionResult, li_xml_temp.start())
        self.proto.x1_queue.put(reqCmd)
        self.tr.clear()
        self.proto.cmd_queue.get().addCallback(self.getCmdData)
        Reason = []        
        def connectionLost(Why):
            Reason.append(Why)
        self.proto.connectionLost = connectionLost
        self.clock.advance(self.proto.timeOut)
        self.assertEqual(1, len(Reason))
        self.assertEqual("Unavailable", self.cmd_data[1].result)
        self.assertEqual(1, len(self.proto._xpathObservers[0]))
        
#     def test_one_ping(self):
#         self.proto.makeConnection(self.tr)
#         self.proto.cmd_queue.get().addCallback(self.getCmdData)
        
#     
#     def test_a_ping(self):
#         self.test_connection()
#         self.proto.sendPingRequest()
#         self.assertIn("pingRequest", self.tr.value())
#         self.tr.clear()
#         (d, _pingCallID) = self.proto.pingResult[0]
#         self.proto.dataReceived(li_xml_temp.X1_Ping_Resp)
#         return self.assertIn('pingResponse', d.result)
#         
#     def test_start_timeout(self):
#         self.proto.timeOut = 1
#         self.test_connection()
#         Start = ReqMsg(expectedRes = X1ProtocolNegotiation.protocolSelectionResult, content = li_xml_temp.start())
#         self.proto.factory.x1_queue.put(Start)
#         (d, _callID) = self.proto.result[0]
#         self.assertIn(X1ProtocolNegotiation.protocolProposal, self.tr.value())
#         self.tr.clear()
#         self.clock.advance(self.proto.timeOut)
#         return self.assertFailure(d, X1ClientTimeoutError)
#         
#     def test_ping_timeout(self):
#         config.ping_delay=1
#         config.ping_timeout=2
#         config.pingEnable = True
#         self.test_connection()
#         self.assertIn("pingRequest", self.tr.value())
#         (d, _pingCallID) = self.proto.pingResult[0]
#         self.tr.clear()
#         self.clock.advance(config.ping_timeout+1)
#         return self.assertFailure(d, X1PingTimeoutError)


