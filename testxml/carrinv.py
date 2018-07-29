'''
Created on 14 lip 2018

@author: m.nowak
'''
import sys

#Most common APIs are available on the ElementTree class

from lxml.etree import ElementTree

#create an ElementTree instance from an XML file

x = ElementTree(file="C:\Users\m.nowak\Desktop\inv\Carrefour\in\SP_100_18_07_000301.xml")



#write out XML from the ElementTree instance

x.write(sys.stdout) 