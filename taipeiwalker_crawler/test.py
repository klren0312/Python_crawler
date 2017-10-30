#!python2.7
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import time
import codecs
import random
import shutil
import requests
from lxml import etree
from collections import OrderedDict
from datetime import datetime, timedelta

#reload(sys)
#sys.setdefaultencoding('utf-8')
#codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)


board = 'TRAVEL'
fileName = 'p4-detail.php_id=2892.txt'
#print board
fileDir = os.getcwd() + '\\' + board + '\\page_content\\'
print fileDir
fileLt = os.listdir(fileDir)
#print fileLt
fileContent = codecs.open('C:/Users/User/Downloads/taipeiwalker_crawler/TRAVEL/page_content/'+fileName, 'r', "utf-8").read()
#print fileContent
tree = etree.HTML(fileContent)
contentElement = tree.xpath('//span[@style="font-size: small;"]')
print contentElement[0]
print unicode(contentElement[0].text,'utf-8')
print len(contentElement)
articleContent = ''.join([i.xpath("normalize-space()") for i in contentElement])
#print len(articleContent)
print articleContent



