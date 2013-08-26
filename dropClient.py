'''
Created on 2013-3-11

@author: ezonghu
'''

from common.multixmlstream import MultiXmlStream

class CmdClientProtocol(MultiXmlStream):
    pass

from twisted.internet.protocol import ClientFactory
class CmdClientFactory(ClientFactory):
    pass

class LiClientProtocol(MultiXmlStream):
    def __init__(self):
        MultiXmlStream.__init__(self)
    def connectionMade(self):
        self.requests = self.factory.requests
        MultiXmlStream.connectionMade( self)
        self.send(self.requests.pop(0))
               
    def onDocumentEnd(self):
        e = self.Elements
        MultiXmlStream.onDocumentEnd(self)
        _Bool, Result= self.check_tuple(u'result', e)
        if u'success' in Result[0]:
            print 'success'
        else:
            print 'failure'
        self.transport.loseConnection()
        from twisted.internet import reactor
        reactor.stop()
        

class LiClientFactory(ClientFactory):
    protocol = LiClientProtocol
    def __init__(self, requests):
        self.requests = requests
        

def LiClient(host, port, requests):
    factory = LiClientFactory(requests)
    from twisted.internet import reactor
    reactor.connectTCP(host, port, factory)
    reactor.run()

import optparse

CmdFormat = {'start' : [],
             'stop' : [],
             'intCfgX2' : [],
             'intCfgX2X3' : [],
             'audReq' : ['uri'],
             'audAll' : [],
             'addTgt' : ['uri', 'ccReq', 'lirid'],
             'remTgt' : ['uri'],
             'updTgt' : ['uri', 'ccReq', 'lirid']}
def parse_args():
    usage = """usage: %prog [options] [hostname]:port
this is the hello client generator.
Run it like this:

    python Client.py -a start 192.168.11.80:5061
it means it  will generate 2 clients and each clients will send 10 hello message to 192.168.11.80:5060
"""
    parser = optparse.OptionParser(usage)
    parser.add_option("-a", "--action", dest="act" , help="please input action type: start|stop|intCfg|audTgt|addTgt|remTgt|updTgt|x2Msgs", default= None)
    parser.add_option("-u", "--uri", dest="uri" , help="please input sip uri", default='')
    parser.add_option("-n", "--num", dest="num" , type="int" , help="please input expected sip message quantity")
    parser.add_option("-c", "--ccReq", dest="ccReq" , action='store_true' , help="if it set, ccReq is enabled", default=False)
    parser.add_option('-l', '--lirid', dest='lirid', type='int', help='please input lirid number')
    options, addresses = parser.parse_args()
   
    if not addresses:
        print parser.format_help()
        parser.exit()
       
    def parse_address(addr):
        if ":" not in addr:
            host= "127.0.0.1"
            port=addr
        else:
            host, port = addr.split( ":", 1 )
       
        if not port.isdigit():
            parser.error( "Ports must be integers." )
           
        return host, int(port)

    if len(addresses) == 0:
        parser.error( "server address is mandatory" )
    else:
        host, port = parse_address(addresses[0])
    
    return host, port, options

def generateCmd(options):
    global CmdFormat
    d = [('action', options.act)]
    for content in CmdFormat[options.act]:
        d.append((content, getattr(options, content, None)))
    from common.multixmlstream import generateXml as xml
    return xml('cmd', d)
    
def main():
    Host, Port, Options = parse_args()
    Cmd = generateCmd(Options)
    print Cmd
    LiClient(Host, Port, [Cmd])
    
    
if __name__ == '__main__':
    main()