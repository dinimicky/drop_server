from twisted.python import failure
from twisted.trial import unittest
from multixmlstream import MultiXmlStream
from twisted.words.xish.xpath import XPathQuery
class MultiXmlStreamTest(unittest.TestCase):
    def setUp(self):
        self.connectionLostMsg = "no reason"
        self.outlist = []
        self.multixmlstream = MultiXmlStream()
        self.multixmlstream.transport = self
        self.multixmlstream.transport.write = self.outlist.append
        
    def loseConnection(self):
        """
        Stub loseConnection because we are a transport.
        """
        self.multixmlstream.connectionLost(failure.Failure(Exception(self.connectionLostMsg)))


    def test_receiveRoot(self):
        """
        Receiving the starttag of the root element results in stream start.
        """
        xmlString = []

        def storeElement(xmlInstance):
            xmlString.append(xmlInstance)
        
        self.multixmlstream.addObserver(XPathQuery("/body/tl"), storeElement)
        self.multixmlstream.connectionMade()
        self.multixmlstream.dataReceived("<root><body><hd/></body><body><tl><bb1/></tl></body>")
        self.multixmlstream.dataReceived('<body><tl><bb2/>Hi</tl></body></root>')
        self.assertEqual(2, len(xmlString))
        self.assertEqual('tl', xmlString[0].children[0].name)
        self.assertEqual('bb1', xmlString[0].children[0].children[0].name)
        self.assertEqual('bb2', xmlString[1].children[0].children[0].name)


