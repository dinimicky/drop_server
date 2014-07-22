'''
Created on 2013-3-11

@author: ezonghu
'''

from common.multixmlstream import MultiXmlStream
from twisted.protocols import policies
from twisted.internet.protocol import ClientFactory
from twisted.python import log
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

class LiClientProtocol(MultiXmlStream, policies.TimeoutMixin):
    def __init__(self):
        self._timeOut = 30
        MultiXmlStream.__init__(self)

        
    def connectionMade(self):
        self.setTimeout(self._timeOut)
        MultiXmlStream.connectionMade(self)
        log.msg("send out cmd req: %s" % self.factory.cmd)
        self.send(self.factory.cmd)    
    
    def onDocumentEnd(self):
        log.msg("recv cmd resp: %s" % self.recvRootElement.toXml())
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
this is the hello client generator.
Run it like this:

    python Client.py -a start 192.168.11.80:5061
it means it  will generate 2 clients and each clients will send 10 hello message to 192.168.11.80:5060
"""
    parser = optparse.OptionParser(usage)
    parser.add_option("-a", "--action", dest="action" , help="please input action type: start|stop|intCfg|audTgt|addTgt|remTgt|updTgt|x2Msgs", default= None)
    parser.add_option("-u", "--uri", dest="uri" , help="please input sip uri", default='')
    parser.add_option("-c", "--ccReq", dest="ccReq" , action='store_true' , help="if it set, ccReq is enabled", default=False)
    parser.add_option('-l', '--lirid', dest='lirid', type='int', help='please input lirid number')
    parser.add_option('-x', '--x2IP', dest='x2IP', help='please input X2 IP Address')
    parser.add_option('-p', '--x2Port', dest='x2Port', type='int', help='please input X2 Port')
    parser.add_option('-X', '--x3IP', dest='x3IP', help='please input X3 IP Address')
    parser.add_option('-P', '--x3Port', dest='x3Port', type='int', help='please input X3 Port')
    
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