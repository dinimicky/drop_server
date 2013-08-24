'''
Created on 2013-7-28

@author: ezonghu
'''
def Indent(dom, node, indent = 0):
    children = node.childNodes[:]
#     print children
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
def toPrettyXml(Filename):                   
    from xml.dom import minidom
    dom = minidom.parse(Filename)
#     print dom
    Indent(dom, dom.documentElement)
    
    prettyxml = ""
    for child in dom.childNodes:
        prettyxml += child.toxml()
        
    return prettyxml 

def test():
    FileName = "test2.xml"
    PrettyXml = toPrettyXml(FileName)
    F = open("Pretty_"+FileName, "w+")
    F.write(PrettyXml)
    F.close()
    
from timeit import Timer
t1 = Timer("test()", "from __main__ import test")
print t1.repeat(1, 1)