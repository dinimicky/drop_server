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
from common.state import State, ReqMsg, RespMsg, X1ProtocolNegotiation
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
        self.assertEqual(0, len(self.proto.factory.cmd_queue.pending))
        self.assertEqual(1, len(self.proto.factory.x1_queue.waiting))
        self.cmd_data = []
        self.assertEqual(0, self.proto.alarmCounter)
            
        
        
    def test_start(self):
        self.proto.makeConnection(self.tr)
        reqCmd = ReqMsg(X1ProtocolNegotiation.protocolSelectionResult, li_xml_temp.start())
        self.proto.factory.x1_queue.put(reqCmd)
        self.assertIn(X1ProtocolNegotiation.protocolProposal, self.tr.value())
        self.tr.clear()
        self.proto.dataReceived(li_xml_temp.Start_Resp)
        self.proto.factory.cmd_queue.get().addCallback(self.getCmdData)
        self.assertIsInstance(self.cmd_data[0], RespMsg)
        self.assertEqual("OK", self.cmd_data[0].result)
        
    def test_start_timeout(self):
        self.proto.makeConnection(self.tr)
        reqCmd = ReqMsg(X1ProtocolNegotiation.protocolSelectionResult, li_xml_temp.start())
        self.proto.factory.x1_queue.put(reqCmd)
        self.tr.clear()
        self.proto.factory.cmd_queue.get().addCallback(self.getCmdData)
        Reason = []        
        def connectionLost(Why):
            Reason.append(Why)
        self.proto.connectionLost = connectionLost
        self.clock.advance(self.proto.timeOut)
        self.assertEqual(1, len(Reason))
        self.assertEqual("Unavailable", self.cmd_data[0].result)
        self.assertEqual(1, len(self.proto._xpathObservers[0]))
        
    def test_one_ping(self):
        self.proto.makeConnection(self.tr)
        self.proto.factory.cmd_queue.get().addCallback(self.getCmdData)
        self.proto._sendPingRequest()
        self.assertIn("pingRequest", self.tr.value())
        self.tr.clear()
        self.assertEqual(2, len(self.proto._xpathObservers[0]))
        self.proto.dataReceived(li_xml_temp.X1_Ping_Resp)
        self.assertEqual(1, len(self.proto._xpathObservers[0]))
        
    def test_ping_timeout(self):     
        self.proto.makeConnection(self.tr)
        self.proto.factory.cmd_queue.get().addCallback(self.getCmdData)
        self.proto._sendPingRequest()
        self.assertIn("pingRequest", self.tr.value())
        self.tr.clear()
        Reason = []
        def connectionLost(Why):
            Reason.append(Why)
        self.proto.connectionLost = connectionLost 
        self.clock.advance(config.ping_timeout)
        self.assertEqual(1, len(Reason))
        
    def test_alarm(self):  
        self.proto.makeConnection(self.tr)
        self.proto.factory.cmd_queue.get().addCallback(self.getCmdData)
        self.proto.dataReceived(li_xml_temp.X1_Alarm)
        self.assertEqual(1, self.proto.alarmCounter)



