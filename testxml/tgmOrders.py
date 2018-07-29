# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from lxml import etree
#import lxml.etree as etree

'''
class ElementTreeCDATA(ET.ElementTree):
    """Subclass of ElementTree which handles CDATA blocks reasonably"""

    def _write(self, file, node, encoding, namespaces):
        """This method is for ElementTree <= 1.2.6"""

        if node.tag == '![CDATA[':
            text = node.text.encode(encoding)
            file.write("\n<![CDATA[%s]]>\n" % text)
        else:
            ET.ElementTree._write(self, file, node, encoding, namespaces)

    def _serialize_xml(write, elem, qnames, namespaces):
        """This method is for ElementTree >= 1.3.0"""

        if elem.tag == '![CDATA[':
            write("\n<![CDATA[%s]]>\n" % elem.text)
        else:
            ET._serialize_xml(write, elem, qnames, namespaces)
'''
'''
ET._original_serialize_xml = ET._serialize_xml

def _serialize_xml(write, elem, encoding, qnames, namespaces):
    if elem.tag == '![CDATA[':
        write("<%s%s]]>%s" % (elem.tag, elem.text, elem.tail))
        return
    return ET._original_serialize_xml(
         write, elem, encoding, qnames, namespaces)
ET._serialize_xml = ET._serialize['xml'] = _serialize_xml
'''

f_in = ('C:\Users\m.nowak\Desktop\inv\ztgm.xml')
f_out = ('C:\Users\m.nowak\Desktop\inv\ztgm1.xml')
f_out2 = ('C:\Users\m.nowak\Desktop\inv\ztgm2.xml')
parser = etree.XMLParser(strip_cdata=False, encoding='utf-8')
tree = ET.parse(f_in, parser=parser)

root = tree.getroot()

# adding an element to the root node
attrib = {}
#element = root.makeelement('seconditems', attrib)
#root.append(element)

# adding an element to the seconditem node
attrib = {}
subelement = root[0][0].makeelement('ExpectedDeliveryTime', attrib)
ET.SubElement(root[0], 'ExpectedDeliveryTime', attrib,)
root[0][4].text = '00:00'

'''
for cdat in tree.findall('.//Line/Line-Item/ItemDescription'): # the tag where my CDATA lives
    cdat.text = etree.CDATA(cdat.text)
#    etree.tostring(cdat, encoding='utf-8')
#    print (cdat.text)
    print(etree.tostring(cdat, encoding='utf-8'))
'''

#for node in tree.findall('.//Line/Line-Item/ItemDescription'):
#    data = node
#    node.append(etree.Comment(' --><![CDATA[' + data.replace(']]>', ']]]]><![CDATA[>') + ']]><!-- '))


# create a new XML file with the new element
tree.write(f_out, encoding='utf-8', xml_declaration=True)

parser = etree.XMLParser(strip_cdata=False)
with open(f_in, "rb") as source:
    tree = etree.parse(source, parser=parser)
etree.SubElement(root, "abc").text = "xyz"    
    
tree.write(f_out2, encoding='utf-8', xml_declaration=True)  

print(root.tag)
for child in root:
    print(child.tag)
  


