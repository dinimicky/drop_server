'''
Created on 2013-3-11

@author: ezonghu
'''

from common.multixmlstream import MultiXmlStream
from twisted.protocols import policies
from twisted.internet.protocol import ClientFactory
Requests = {'start': '<cmd> <action>start</action></cmd> ',
            'intCfgX2':' <cmd><action>intCfgX2</action><x2IP>127.0.0.1</x2IP><x2Port>22345</x2Port> </cmd>',
            'intCfgX2X3':' <cmd><action>intCfgX2X3</action> </cmd>',
            'addTgt':' <cmd><action>addTgtUri</action> <uri>sip:123@163.com</uri><lirid>123</lirid> <ccReq>true</ccReq></cmd> ',
            'audAll':' <cmd><action>audAllTgt</action></cmd> ',
            'audReq':' <cmd><action>audTgtUri</action> <uri>sip:123@163.com</uri></cmd> ',
            'updTgt':' <cmd><action>updTgtUri</action> <uri>sip:123@163.com</uri><lirid>123</lirid> <ccReq>false</ccReq></cmd> ',
            'remTgt':' <cmd><action>remTgtUri</action> <uri>sip:123@163.com</uri></cmd>',
            'addTgtW':' <cmd><action>addTgtWildcardUri</action> <wuri>sip:123@163.com</wuri><lirid>123</lirid> <ccReq>true</ccReq></cmd> ',
            'audReqW':' <cmd><action>audTgtWildcardUri</action> <wuri>sip:123@163.com</wuri></cmd> ',
            'updTgtW':' <cmd><action>updTgtWildcardUri</action> <wuri>sip:123@163.com</wuri><lirid>123</lirid> <ccReq>false</ccReq></cmd> ',
            'remTgtW':' <cmd><action>remTgtWildcardUri</action> <wuri>sip:123@163.com</wuri></cmd>',
            'addTgtF':' <cmd><action>addTgtFNI</action> <fni>sip:123@163.com</fni><lirid>123</lirid> <ccReq>true</ccReq></cmd> ',
            'audReqF':' <cmd><action>audTgtFNI</action> <fni>sip:123@163.com</fni></cmd> ',
            'updTgtF':' <cmd><action>updTgtFNI</action> <fni>sip:123@163.com</fni><lirid>123</lirid> <ccReq>false</ccReq></cmd> ',
            'remTgtF':' <cmd><action>remTgtFNI</action> <fni>sip:123@163.com</fni></cmd>',
            'stop':' <cmd><action>stop</action> </cmd>',
            }

class CaseInfo(object):
    CasePrefix = 'tg-'
    TargetTypes = {'1':'uri', '2':'wuri', '3':'fni'}
    def __init__(self, caseDir):
        self.caseDir = caseDir
    def parseCaseInfoString(self, CaseInfoStr):
        CaseInfoList = CaseInfoStr.split('_')
        self.caseFileName = self.caseDir+'/'+CaseInfo.CasePrefix+CaseInfoList[0]
        self.targetType = CaseInfo.TargetTypes[CaseInfoList[1]]
        self.liridBaseNum = int(CaseInfoList[2]) if CaseInfoList[2].isdigit() else ''
        self.ccReq = CaseInfoList[3]
        
    def parseCaseFile(self):
        pass
        
        
class LiClientProtocol(MultiXmlStream, policies.TimeoutMixin):
    def __init__(self):
        self._timeOut = 30
        MultiXmlStream.__init__(self)

        
    def connectionMade(self):
        self.setTimeout(self._timeOut)
        MultiXmlStream.connectionMade(self)
        print("send out cmd req: %s" % self.factory.cmd)
        self.send(self.factory.cmd)    
    
    def onDocumentEnd(self):
        print("recv cmd resp: %s" % self.recvRootElement.toXml())
        self.transport.loseConnection()

class LiClientFactory(ClientFactory):
    protocol = LiClientProtocol
    def __init__(self, cmd):
        self.cmd = cmd
        

def LiClient(host, port, requests):
    factory = LiClientFactory(requests)
    from twisted.internet import reactor
    reactor.connectTCP(host, port, factory)
    reactor.run()

import optparse

from common import config
def parse_args():
    usage = """usage: %prog [options] [hostname]:port
Run it like this:

    python Client.py -a start -n 2.3.1_1_123_true 127.0.0.1:33333
it means the client will send cmd xml string with start action to the server 127.0.0.1:33333
"""
    parser = optparse.OptionParser(usage)
    parser.add_option("-a", "--action", dest="action" , 
                      help = "please input action type: %s " % ([k for k in config.ActionDict]))
    parser.add_option("-n", "--caseinfo", dest="caseInfo" , help="please input case information")
    parser.add_option("-d", "--dir", dest="caseDir" , help="please input case directory")
    parser.add_option('-x', '--xiiIP', dest='x2IP', help='please input XII IP Address')
    parser.add_option('-p', '--xiiPort', dest='x2Port', type='int', help='please input XII Port')
    parser.add_option('-X', '--xiiiIP', dest='x3IP', help='please input XIII IP Address')
    parser.add_option('-P', '--xiiiPort', dest='x3Port', type='int', help='please input XIII Port')
    
    options, addresses = parser.parse_args()
   
    if not addresses:
        print parser.format_help()
        parser.exit()
       
    def parse_address(addr):
        if ":" not in addr:
            host= "127.0.0.1"
            port=addr
        else:
            host, port = addr.rsplit( ":", 1 )
       
        if not port.isdigit():
            parser.error( "Ports must be integers." )
           
        return host, int(port)

    if len(addresses) == 0:
        parser.error( "server address is mandatory" )
    else:
        host, port = parse_address(addresses[0])
    
    return host, port, options

def generateCmd(options):
    from dropcmd.cmdcallbacks import CmdReq
    action = options.action
    args = config.ActionDict[action]
    kwargs = {}
    
    if options.caseDir :
        caseInfo = CaseInfo(options.caseDir)
        
    if options.caseInfo:
        caseInfo = CaseInfo()
        caseInfo.parseCaseInfoString(options.caseInfo)
    
    for arg in args:
        if 'IP' in arg:
            kwargs[arg] = config.convertip(getattr(options, arg))
            continue
        kwargs[arg] = getattr(options, arg)
        
    return CmdReq(action, args, **kwargs).toXml()
    
    
    
def main():
    Host, Port, Options = parse_args()
    Cmd = generateCmd(Options)
    LiClient(Host, Port, Cmd)
    
    
if __name__ == '__main__':
    main()