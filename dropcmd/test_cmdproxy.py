'''
Created on 2013-2-28

@author: ezonghu
'''
from twisted.internet import protocol, defer
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
        cmdFac = newCmdProxyFactory()

        self.cmdProto = cmdFac.buildProtocol(('127.0.0.1', 0))
        self.cmd_tr.protocol = self.cmdProto
        
        self.cmdProto.makeConnection(self.cmd_tr)
        def start_x1_client():
            x1fac = x1client.X1ClientFactory(self.cmdProto.factory.cmd_queue, 
                                             self.cmdProto.factory.x1_queue, 
                                             self.cmdProto.factory.state)
            self.x1Proto = x1fac.buildProtocol(('127.0.0.1', 0))
            self.cmd_tr.protocol = self.x1Proto
            self.x1Proto.makeConnection(self.x1_tr)
        self.cmdProto._start_x1_client = start_x1_client
            
    def tearDown(self):
        pass
        
    def test_start(self):
        self.cmdProto.dataReceived(Requests['start'])
        self.assertIn('protocolProposal', self.x1_tr.value())
        log.msg("x1client send out: start\n %s" % self.x1_tr.value())
        self.x1_tr.clear()
        self.x1Proto.dataReceived(li_xml_temp.Start_Resp)
        log.msg("cmdclient send out: %s" % self.cmd_tr.value())
        self.assertIn("success", self.cmd_tr.value())
        self.cmd_tr.clear()
        

#    def test_start(self):
#        def createprotocolNegotiation():
#            from lixml import li_lic as lic
#            prt = lic.protocolProposal(lic.LIC_ProtocolProposal(config.LI_ADM_ObjectId, lic.ProtocolVersion(minor=0)) + 
#                                       lic.LIC_ProtocolProposal(config.LI_IRI_ObjectId, lic.ProtocolVersion(minor=0)) +
#                                       lic.LIC_ProtocolProposal(config.LI_CC_ObjectId, lic.ProtocolVersion(minor=0)))
#            return lic.LIC_Msg(config.Lic_ObjectId, config.Lic_ProtObjectId, '<protocolSelectionResult>'+prt+'</protocolSelectionResult>')
#        self.liServer.cmd = createprotocolNegotiation()
#        d = LiClient(config.ipAddress_LITT, config.cmdServerPort, Test.Requests[:2])
#        def get_resp(Keys):
#            log.msg("recv key: %s" % str(Keys))
#            for (k, v) in Keys:
#                if 'result'== k:
#                    log.msg('get result: %s:%s' % (k, v[0]))
#                    self.assertEqual("success", v[0])
#                    return
#            self.fail(Keys)
#        return d.addCallback(get_resp)
                  

    

