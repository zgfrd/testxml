import sys
import lxml.etree as ET
#using lxml instead of xml preserved the comments

#adding the encoding when the file is opened and written is needed to avoid a charmap error
with open("C:\Users\m.nowak\Desktop\inv\Carrefour\in\SP_100_18_07_000301.xml") as f:
    tree = ET.parse(f)
    root = tree.getroot()
    
    for elem in root.getiterator():
        try:
            d = tree.find('Document-Invoice/Invoice-Header/InvoiceNumber')
#            elem.text = elem.text.replace('FEATURE NAME', 'THIS WORKED')
#            elem.text = elem.text.replace('FEATURE NUMBER', '123456')
        except AttributeError:
            pass

#tree.write('output.xml', encoding="utf8")
# Adding the xml_declaration and method helped keep the header info at the top of the file.
#tree.write('C:\Users\m.nowak\Desktop\inv\Carrefour\in\output.xml', xml_declaration=True, method='xml', encoding="utf8")
tree.write(sys.stdout) 
