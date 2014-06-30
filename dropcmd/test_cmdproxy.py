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
    
    def start_x1_client(self):
        return
    
class CmdProxyTest(unittest.TestCase):

    def setUp(self):
        config.pingEnable = False
        self.cmd_tr = proto_helpers.StringTransportWithDisconnection()
        self.x1_tr = proto_helpers.StringTransportWithDisconnection()
        cmdFac = newCmdProxyFactory()
        
        self.cmdProto = cmdFac.buildProtocol(('127.0.0.1', 0))
        self.cmdProto.makeConnection(self.cmd_tr)
        
        def start_x1_client():
            self.x1Proto = cmdFac.x1CliFac.buildProtocol(('127.0.0.1', 0))
            self.x1Proto.makeConnection(self.x1_tr)
        
        cmdFac.start_x1_client = start_x1_client
        class dummyX1TCP(object):
            def disconnect(self):
                return
        cmdFac.x1tcp = dummyX1TCP()
                   
    def test_start(self):
        self.cmdProto.dataReceived(Requests['start'])
        self.assertIn('protocolProposal', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.Start_Resp)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
        
    def test_intCfgX2(self):
        self.test_start()
        self.cmdProto.dataReceived(Requests['intCfgX2'])
        self.assertIn('x2InterfaceAddress', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.IntCfgX2_Resp)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
  
    def test_intCfgX2X3(self):
        self.test_start()
        self.cmdProto.dataReceived(Requests['intCfgX2X3'])
        self.assertIn('x3InterfaceAddress', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.IntCfgX2X3_Resp)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
 
    def test_addTgtUri(self):
        self.test_start()
        self.cmdProto.dataReceived(Requests['addTgt'])
        self.assertIn('addTargetRequest', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.AddTgtUri_Resp_OK)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
         
    def test_remTgtUri(self):
        self.test_start()
        self.cmdProto.dataReceived(Requests['remTgt'])
        self.assertIn('removeTargetRequest', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.RemTgtUri_Resp_OK)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
         
    def test_audTgtUri(self):
        self.test_start()
        self.cmdProto.dataReceived(Requests['audReq'])
        self.assertIn('auditRequest', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.AudTgtUri_Resp_OK)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
        
    def test_audAllTgt(self):
        self.test_start()
        self.cmdProto.dataReceived(Requests['audAll'])
        self.assertIn('allTargets', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.AudTgtUri_Resp_OK)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
        
    def test_udpTgtUri(self):
        self.test_start()
        self.cmdProto.dataReceived(Requests['updTgt'])
        self.assertIn('updateTargetRequest', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.UpdTgtUri_Resp_OK)
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()        
        
    def test_stop(self):
        self.test_start()
        self.cmdProto.dataReceived(Requests['stop'])
        self.assertIn('endSessionRequest', self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.Stop_Resp)
        self.assertIn("endSessionAck", self.cmd_tr.value())
        self.cmd_tr.clear()        
                
        