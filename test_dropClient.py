'''
Created on 2013-8-29

@author: ezonghu
'''
import dropClient
from twisted.trial import unittest
from twisted.internet import task
from twisted.test import proto_helpers
from dropClient import LiClientFactory
class DropClientTest(unittest.TestCase):


    def setUp(self):
        self.tr = proto_helpers.StringTransportWithDisconnection()
        self.clock = task.Clock()
        factory = LiClientFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr.protocol = self.proto
        self.proto.callLater = self.clock.callLater
     
    def _sendCmd(self, cmd):
        self.proto.factory.requests = [cmd]
        self.proto.makeConnection(self.tr)
        def lost():
            return
        self.proto.transport.loseConnection = lost   
        
    def _sendResp(self, result, comment):
        Resp = '<cmd><result>%s</result><comment>%s</comment></cmd>' % (result, comment)
        self.proto.dataReceived(Resp)
        
    def test_start(self):
        cmd = dropClient.Requests['start']
        self._sendCmd(cmd)
        self.assertIn('start', self.tr.value())
        
    def test_result_success(self):
        self.test_start()
        self._sendResp("success", "test start")
        
        self.assertIn("success", str(self.proto.resp))
        
    def test_result_failure(self):
        self.test_start()

        self._sendResp("failure", "test start")
        
        self.assertIn("failure", str(self.proto.resp))
