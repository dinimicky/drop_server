'''
Created on 2013-8-29

@author: ezonghu
'''
import dropClient
from twisted.trial import unittest
from twisted.internet import task
from twisted.test import proto_helpers
from dropClient import LiClientFactory
import sys
from twisted.python import log
log.startLogging(sys.stdout)

FileContent = '''[uri]
TEL:+86690000008001
[wuri]
TEL:888*
[fni]
PSTN-Route
'''
class DropCliParseArgTest(unittest.TestCase):
    def setUp(self):
        with open('tg-2.0.1', 'w') as f:
            f.write(FileContent)
    def tearDown(self):
        import os
        os.remove('tg-2.0.1')
    
    def sut(self):
        host, port, options = dropClient.parse_args()
        return host, port, dropClient.generateCmd(options)
    
    def set_input_args(self, string):
        sys.argv = ['mock'] + string.split()
        
    def test_parse_start(self):
        self.set_input_args('-a start 127.0.0.1:3333')
        host, port, cmds = self.sut()
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 3333)
        self.assertEqual(cmds[0], dropClient.Requests['start'])

    def test_parse_stop(self):
        self.set_input_args('-a stop 127.0.0.1:3333')
        host, port, cmds = self.sut()
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 3333)
        self.assertEqual(cmds[0], dropClient.Requests['stop'])

    def test_parse_intCfgX2(self):
        self.set_input_args('-a intCfgX2 -x 127.0.0.1 -p 22345 127.0.0.1:3333')
        host, port, cmds = self.sut()
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 3333)
        self.assertEqual(cmds[0], dropClient.Requests['intCfgX2'])
        
    def test_parse_intCfgX2X3(self):
        self.set_input_args('-a intCfgX2X3 -x 127.0.0.1 -p 22345 -X 127.0.0.1 -P 32345 127.0.0.1:3333')
        host, port, cmds = self.sut()
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 3333)
        self.assertEqual(cmds[0], dropClient.Requests['intCfgX2X3'])
    
    def test_parse_addTgtUri(self):
        self.set_input_args('-a addTgtUri -n 2.0.1_0_1_true 127.0.0.1:3333')
        host, port, cmds = self.sut()
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 3333)
        self.assertEqual(cmds[0], dropClient.Requests['addTgt'])

    def test_parse_addTgtWildcardUri(self):
        self.set_input_args('-a addTgtWildcardUri -n 2.0.1_1_1_true 127.0.0.1:3333')
        host, port, cmds = self.sut()
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 3333)
        self.assertEqual(cmds[0], dropClient.Requests['addTgtW'])            

    def test_parse_addTgtFNI(self):
        self.set_input_args('-a addTgtFNI -n 2.0.1_2_1_true 127.0.0.1:3333')
        host, port, cmds = self.sut()
        self.assertEqual(host, '127.0.0.1')
        self.assertEqual(port, 3333)
        self.assertEqual(cmds[0], dropClient.Requests['addTgtF'])          
        
    def test_parse_addTgtWildcardUri_wrongType(self):
        self.set_input_args('-a addTgtWildcardUri -n 2.0.1_0_1_true 127.0.0.1:3333')
        self.assertRaises(dropClient.TargetTypeMisatchError, self.sut) 

            

        
class DropClientTest(unittest.TestCase):

    def setUp(self):
        self.tr = proto_helpers.StringTransportWithDisconnection()
        self.clock = task.Clock()

     
    def _sendCmds(self, cmds):
        factory = LiClientFactory(cmds)
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr.protocol = self.proto
        self.proto.callLater = self.clock.callLater
        self.proto.factory.cmds = cmds
        self.proto.makeConnection(self.tr)
        def lost():
            return
        self.proto.transport.loseConnection = lost   
        
    def _sendResp(self, result, comment):
        Resp = '<cmd><result>%s</result><comment>%s</comment></cmd>' % (result, comment)
        self.proto.dataReceived(Resp)
        
    def test_start(self):
        cmd = dropClient.Requests['start']
        self._sendCmds([cmd])
        self.assertIn('start', self.tr.value())
        
    def test_result_success(self):
        self._sendCmds([dropClient.Requests['start']])
        self._sendResp("success", "test start")
        self.assertIn("success", str(self.proto.recvRootElement.toXml()))
         
    def test_result_failure(self):
        self.test_start()
        self._sendResp("failure", "test start")
        self.assertIn("failure", str(self.proto.recvRootElement.toXml()))

        