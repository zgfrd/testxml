# -*- coding: utf-8 -*-
from lxml import etree
import os, shutil, datetime
from __builtin__ import str
from logging import exception

# path = i_ input files, t_ temp where write files, o_ output files, a_ archive folder where i_ moving after parsing. Use r parameter for relative path
i_path = ('C:\Users\m.nowak\Desktop\inv')
t_path = (r'C:\Users\m.nowak\Desktop\inv\tmp')
o_path = ('C:\Users\m.nowak\Desktop\out')
a_path = ('C:\Users\m.nowak\Desktop\inv\dupa')

# loop for infiles
for files in os.listdir(i_path):
    current_files = os.path.join(i_path, files)
    if os.path.isdir(current_files):
        # skip directories
        continue

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  i_fParse <- ' + current_files)

    parser = etree.XMLParser(strip_cdata=False, remove_blank_text=True)
    with open(current_files, "rb") as source:
        doc = etree.parse(source, parser=parser)

    root = doc.getroot()

    # remove slashes from InvoiceNumber
    invoiceNumber = root.xpath('//Invoice-Header/InvoiceNumber')
    if invoiceNumber:
        invNum = invoiceNumber[0].text.replace('/', '')
        invoiceNumber[0].text = invNum
    
    # remove slashes from InvoiceReferenceNumber
    invoiceReferenceNumber = root.xpath('//Invoice-Header/Reference/InvoiceReferenceNumber')
    if invoiceReferenceNumber:
        invRefNum = invoiceReferenceNumber[0].text.replace('/', '')    
        invoiceReferenceNumber[0].text = invRefNum
    

    buyerOrderNumber = root.xpath('//Invoice-Header/Order/BuyerOrderNumber')
    bOnr = buyerOrderNumber[0].text
    buyerOrderDate = root.xpath('//Invoice-Header/Order/BuyerOrderDate')
    bOdt = buyerOrderDate[0].text
#    try:
#        if bOnr:
#            except:
#                print('brak nr zam')
#                print("Unexpected error:"), sys.exc_info()[0]
#            #raise

#    czypusty = bOnr.isspace()
#    print czypusty
        
    if bOnr and (not bOnr.isspace()):
        pass #print bOnr
    else:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  i_fPaErr !- ' + 'Brak nr zapotrzebaowania klienta <BuyerOrderNumber>, faktura: ' + invoiceNumber[0].text)
    
    if bOdt and (not bOdt.isspace()):
        pass #print bOdt
    else:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  i_fPaErr !- ' + 'Brak daty zamowienia klienta <BuyerOrderDate>, faktura: ' + invoiceNumber[0].text)

    try:
        jestNr = bOnr and (not bOnr.isspace())
        print('nrOK: ') + str(jestNr)
        jestDt = bOdt and (not bOdt.isspace())
        print('dtOK: ') + str(jestDt)
    except:
        if not jestNr:
            print('brakNr')
        if not jestDt:
            print('brakDt')
    
    # copy payer to buyer
    bILN = root.xpath('//Invoice-Parties/Buyer/ILN')
    bTaxID = root.xpath('//Invoice-Parties/Buyer/TaxID')
    bAccountNumber = root.xpath('//Invoice-Parties/Buyer/AccountNumber')
    bName = root.xpath('//Invoice-Parties/Buyer/Name')
    bStreetAndNumber = root.xpath('//Invoice-Parties/Buyer/StreetAndNumber')
    bCityName = root.xpath('//Invoice-Parties/Buyer/CityName')
    bPostalCode = root.xpath('//Invoice-Parties/Buyer/PostalCode')
    bCountry = root.xpath('//Invoice-Parties/Buyer/Country')
    
    pILN = root.xpath('//Invoice-Parties/Payer/ILN')
    pTaxID = root.xpath('//Invoice-Parties/Payer/TaxID')
    pAccountNumber = root.xpath('//Invoice-Parties/Payer/AccountNumber')
    pName = root.xpath('//Invoice-Parties/Payer/Name')
    pStreetAndNumber = root.xpath('//Invoice-Parties/Payer/StreetAndNumber')
    pCityName = root.xpath('//Invoice-Parties/Payer/CityName')
    pPostalCode = root.xpath('//Invoice-Parties/Payer/PostalCode')
    pCountry = root.xpath('//Invoice-Parties/Payer/Country')  
  
    if bILN:
        bILN[0].text = pILN[0].text
     
    if bTaxID:
        bTaxID[0].text = pTaxID[0].text

    if bAccountNumber:
        bAccountNumber[0].text = pAccountNumber[0].text
    
    if bName:
        bName[0].text = pName[0].text

    if bStreetAndNumber:
        bStreetAndNumber[0].text = pStreetAndNumber[0].text
     
    if bCityName:
        bCityName[0].text = pCityName[0].text
     
    if bPostalCode:
        bPostalCode[0].text = pPostalCode[0].text
     
    if bCountry:
        bCountry[0].text = pCountry[0].text

    # add subelement UtilizationRegisterNumber (if not exists)
    UtilizationRegisterNumber = root.xpath('//Invoice-Parties/Seller/UtilizationRegisterNumber')
    if not UtilizationRegisterNumber:
        BDO = 'BDO 000025554'
        etree.SubElement(root[1][3], 'UtilizationRegisterNumber')
        UtilizationRegisterNumber = root.xpath('//Invoice-Parties/Seller/UtilizationRegisterNumber')
        if UtilizationRegisterNumber:
            UtilizationRegisterNumber[0].text = BDO

    # remove [] from Invoice-Lines/Line/Line-Item/ItemDescription and cut to 70 letters
    count = 0
           
    for a in root.xpath('//Invoice-Lines/Line/Line-Item/ItemDescription'):
        x = a.text.replace('[', '').replace(']', '')[0:70]

        itemDescription = root.xpath('//Invoice-Lines/Line/Line-Item/ItemDescription')
        if itemDescription:
            itemDescription[count].text = etree.CDATA(x)
            count = count + 1

    #outFile = open(current_files.replace('.xml', '_parse.xml'), 'w')

    # write outfile to tmp folder
    pF = (t_path) + '\\' + (os.path.basename(current_files))
    outFile = open(pF,'w')
    doc.write(outFile, encoding='utf-8', xml_declaration=True, pretty_print=True)
    outFile.close()
 
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  t_fWrite -> ' + pF)

    # move from tmp to out folder
    #os.rename(current_files, a_file)
    # or shutil.move() [import shutil] shutil.move simply calls os.rename in most cases. However, if the destination is on a different disk than the source, it will instead copy and then delete the source file.
    o_file = (o_path) + '\\' + (os.path.basename(current_files))
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  o_tfMove -> ' + pF + ' -> '  + o_file)
#    shutil.move(pF, o_file)

    # move infile to archive folder
    a_file = (a_path) + '\\' + (os.path.basename(current_files))
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  a_ifMove -> ' + current_files + ' -> '  + a_file)
#    shutil.move(current_files, a_file)
    #print(len(parser.error_log)) 

