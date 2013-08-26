from twisted.words.xish import xmlstream
import types

class XmlGenerator(object):
    def __init__(self, root, withRoot=True, contents=[]):
        self.root = root
        self.withRoot = withRoot
        self.content = contents
        
    def toXml(self):
        childFormat=""
        for e in self.content:
            if types.TupleType == type(e):
                k, v = e
                if None == v:
                    if None == k:
                        continue
                    else:
                        childFormat += "<%s/>" % str(k)
                        continue
                childFormat += "<%s>%s</%s>" % (str(k), str(v), str(k))
            elif type(e) in types.StringTypes:                
                childFormat += "%s" % str(e)
                continue   
        if self.root != '' and True == self.withRoot:
            return "<%s>%s</%s>" % (str(self.root), str(childFormat), str(self.root))
        else:
            return str(childFormat)
    def toPrettyXml(self):
        string = self.toXml()
        import xml.dom.minidom
        def Indent(dom, node, indent = 0):
            children = node.childNodes[:]
            if indent:
                text = dom.createTextNode('\n' + '\t' * indent)
                node.parentNode.insertBefore(text, node)
            if children:
                if children[-1].nodeType == node.ELEMENT_NODE:
                    text = dom.createTextNode('\n' + '\t' * indent)
                    node.appendChild(text)
                for n in children:
                    if n.nodeType == node.ELEMENT_NODE:
                        Indent(dom, n, indent + 1)
                        
        dom = xml.dom.minidom.parseString(string)
        Indent(dom, dom.documentElement)
        prettyxml = ""
        for child in dom.childNodes:
            prettyxml += child.toxml()
            
        return prettyxml           
def toPrettyXml(string):
    def Indent(dom, node, indent = 0):
        children = node.childNodes[:]
        if indent:
            text = dom.createTextNode('\n' + '\t' * indent)
            node.parentNode.insertBefore(text, node)
        if children:
            if children[-1].nodeType == node.ELEMENT_NODE:
                text = dom.createTextNode('\n' + '\t' * indent)
                node.appendChild(text)
            for n in children:
                if n.nodeType == node.ELEMENT_NODE:
                    Indent(dom, n, indent + 1)
                    
    from xml.dom import minidom
    dom = minidom.parseString(string)
    Indent(dom, dom.documentElement)
    
    prettyxml = ""
    for child in dom.childNodes:
        prettyxml += child.toxml()
        
    return prettyxml    

def generateXml(root, content=[]):
    childFormat=""
    for e in content:
        if types.TupleType == type(e):
            k, v = e
            if None == v:
                if None == k:
                    continue
                else:
                    childFormat += "<%s/>" % str(k)
                    continue
            childFormat += "<%s>%s</%s>" % (str(k), str(v), str(k))
        elif type(e) in types.StringTypes:                
            childFormat += "%s" % str(e)
            continue   
    if root != '':
        return "<%s>%s</%s>" % (str(root), str(childFormat), str(root))
    else:
        return str(childFormat)    





def generateXmlFromList(elements):
    if [] == elements:
        return ''
    Format = ""
    for Context in elements:
        if type(Context) in types.StringTypes:
            Format += str(Context)
        elif types.TupleType == type(Context):
            (ChildTag, ChildCtxs) = Context
            ChildTag = str(ChildTag)
            Format += "<%s>%s</%s>" % (ChildTag, generateXmlFromList(ChildCtxs), ChildTag)
        else:
            Format += str(Context)        

    return Format
            
                

class MultiXmlStream(xmlstream.XmlStream):
    def __init__(self):
        self.Elements = []
        xmlstream.XmlStream.__init__(self)   
        
    def onDocumentEnd(self):
        '''
        onDocumentEnd in XmlStream will close the connection
        MultiXmlStream should receive multi-Xml streams.
        So after a document receive, the stream will be initialized to receive a new document
        '''
        self.Elements=[]
        self.dispatch(self, xmlstream.STREAM_END_EVENT)
        self._initializeStream()
       
    def onElement(self, element):
        def store_element(Msg, element):
            children = []
            for child in element.children:
                if type(child) == types.UnicodeType:
                    cleanchild = ''.join(child.split())
                    if cleanchild != '':
                        children.append(child)
                elif child.__class__.__name__ is 'Element':
                    children.extend(store_element([], child))
                else:
                    children.append(child)

            Msg.append((element.name, children))
            return Msg

        store_element( self.Elements, element)

        return xmlstream.XmlStream.onElement( self, element)
   
    def check_tuple(self, Node, Tuples):
        Bool = False
        Result = []
        for (Key, values) in Tuples:
            if Key == Node:
                Bool = True
                Result.append(values)
           
        return (Bool, Result)
    
    def Elements2Xml(self):
        pass


def test_generateXmlFromList():
    print generateXmlFromList([("a", []),("b", [("c", [1])]), ('d', [])])
if __name__ == "__main__":
    test_generateXmlFromList()