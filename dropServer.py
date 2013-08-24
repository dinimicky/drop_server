'''
Created on 2013-3-11

@author: ezonghu
'''


def main():
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)
    from dropcmd import cmdproxy
    from common import config
    from twisted.internet import reactor
    factory = cmdproxy.CmdProxyFactory()
    reactor.listenTCP(config.cmdServerPort, factory, interface = config.ipAddress_LITT)
    log.msg('start to runing dropServer')
    reactor.run()
    
if __name__ == '__main__':
    main()