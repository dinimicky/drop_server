from twisted.words.xish import xmlstream               
class MultiXmlStream(xmlstream.XmlStream):
    def onDocumentStart(self, rootElement):
        self.recvRootElement = rootElement
        xmlstream.XmlStream.onDocumentStart(self, rootElement)
    
    def onElement(self, element):
        self.recvRootElement.addChild(element)
        xmlstream.XmlStream.onElement(self, element)
    def onDocumentEnd(self):
        '''
        onDocumentEnd in XmlStream will close the connection
        MultiXmlStream should receive multi-Xml streams.
        So after a document receive, the stream will be initialized to receive a new document
        '''
        self.dispatch(self, xmlstream.STREAM_END_EVENT)
        self._initializeStream()
        self.recvRootElement = None
       
