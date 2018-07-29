# -*- coding: utf-8 -*-
from lxml import etree
import os, shutil

# path = i_ input for files, o_ for output files, a_ archive folder where i_ moving after parsing. Use r parameter for relative path
i_path = ('C:\Users\m.nowak\Desktop\inv\zam')
o_path = ('C:\Users\m.nowak\Desktop\out')
a_path = ('C:\Users\m.nowak\Desktop\inv\zam\dupa')

# loop for infiles
for files in os.listdir(i_path):
    current_files = os.path.join(i_path, files)
    if os.path.isdir(current_files):
        # skip directories
        continue

    print('in <- ' + current_files)

    '''
    f_in = ('C:\Users\m.nowak\Desktop\inv\ztgm.xml')
    f_out = ('C:\Users\m.nowak\Desktop\inv\ztgm1.xml')
    '''
    parser = etree.XMLParser(strip_cdata=False, remove_blank_text=True)
    with open(current_files, "rb") as source:
        doc = etree.parse(source, parser=parser)

    root = doc.getroot()

    '''
    print(root.tag)
    for child in root:
        print(child.tag)
    
    doc.find('.Order-Header/OrderNumber')
    
    #dlvt = etree.SubElement(root[0][3], 'ExpectedDeliveryTime')
    '''
    # add subelement
    etree.SubElement(root[0], 'ExpectedDeliveryTime')
    root[0][4].text = '00:00'

    '''
    attrib = {}
    subelement = root[0][0].makeelement('ExpectedDeliveryTime', attrib)
    etree.SubElement(root[0], 'ExpectedDeliveryTime', attrib,)
    root[0][4].text = '00:00'
    
    #print etree.tostring(doc, pretty_print=True)
    '''

    #outFile = open(current_files.replace('.xml', '_parse.xml'), 'w')

    # write outfile
    pF = (o_path) + '\\' + (os.path.basename(current_files))
    outFile = open(pF,'w')
    doc.write(outFile, encoding='utf-8', xml_declaration=True, pretty_print=True)
    outFile.close()
    '''
    #print(os.path.basename(current_files))
    #print(o_path + "\\" + os.path.basename(current_files))
    '''
    print('out -> ' + pF)

    # move infile to archive folder
    a_file = (a_path) + '\\' + (os.path.basename(current_files))
    #os.rename(current_files, a_file)
    shutil.move(current_files, a_file)
    # or shutil.move() [import shutil] shutil.move simply calls os.rename in most cases. However, if the destination is on a different disk than the source, it will instead copy and then delete the source file.
    print('moving to archive ' + current_files + ' -> '  + a_file)


