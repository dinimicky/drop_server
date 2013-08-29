'''
Created on 2013-2-28

@author: ezonghu
'''

from common import config
from dropClient import Requests
from twisted.trial import unittest
from dropcmd import cmdproxy
from li import x1client
from lixml import li_xml_temp
from twisted.python import log
from twisted.test import proto_helpers
import sys

log.startLogging(sys.stdout)

class newCmdProxyFactory(cmdproxy.CmdProxyFactory):
    def _start_x2_server(self):
        return
class CmdProxyTest(unittest.TestCase):

    def setUp(self):
        config.pingEnable = False
        self.cmd_tr = proto_helpers.StringTransportWithDisconnection()
        self.x1_tr = proto_helpers.StringTransportWithDisconnection()
        self.cmdFac = newCmdProxyFactory()
        self.cmdConnection()
    def cmdConnection(self):
        self.cmdProto = self.cmdFac.buildProtocol(('127.0.0.1', 0))
        self.cmd_tr.protocol = self.cmdProto
        
        self.cmdProto.makeConnection(self.cmd_tr)
        def start_x1_client():
            x1fac = x1client.X1ClientFactory(self.cmdProto.factory.cmd_queue, 
                                             self.cmdProto.factory.x1_queue, 
                                             self.cmdProto.factory.state)
            self.x1Proto = x1fac.buildProtocol(('127.0.0.1', 0))
            self.cmd_tr.protocol = self.x1Proto
            self.x1Proto.makeConnection(self.x1_tr)
        self.cmdProto._start_x1_connection = start_x1_client
            
    def tearDown(self):
        pass
        
    def test_start(self):
        self.cmdProto.dataReceived(Requests['start'])
        self.assertIn('protocolProposal', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.Start_Resp)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
        
    def test_intCfgX2_success(self):
        self.test_start()
        self.cmdConnection()
        self.cmdProto.dataReceived(Requests['intCfgX2'])
        self.assertIn('interfConfRequest', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.IntCfgX2_Resp)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()

    def test_intCfgX2X3_success(self):
        self.test_start()
        self.cmdConnection()
        self.cmdProto.dataReceived(Requests['intCfgX2X3'])
        self.assertIn('interfConfRequest', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.IntCfgX2X3_Resp)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
