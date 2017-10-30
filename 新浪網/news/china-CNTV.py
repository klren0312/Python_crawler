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




class test:

    def __init__(self):
        self.name = 'CNTV'
        self.logName = 'CNTV_crawler'
        self.currentDateObject = "null"

    def writeTxt(self, fileName, content, method='a'):
        file = open(fileName,method)
        file.write(content + '\n')
        file.close()


    def getlink(self,url):
url = 'http://www.news.cn/fortune/'
response = requests.get(url)
print response.status_code


tree = etree.HTML(response.text)
        #print response.text
searchResult = tree.xpath('//li[@class="clearfix"]/h3/a')  #尋找所需要的url
print searchResult

for i in searchResult:              #只需要href的內文當url
    print i.get('href')

urlLt = []
for i in searchResult:
    urlLt.append(i.get('href')) ##將結果存入urlLt
print urlLt

for i in range(len(urlLt)):             #依照urlLt陣列裡有多少url就跑幾次
    response = requests.get(urlLt[i])
    print response.text
    time.sleep(random.randint(1,3))

        for i in searchResult:              ##把找到的href加進urlLt陣列裡
            urlLt.append(i.get('href'))
        print urlLt





        return urlLt



    def getcontent(self):           #取得網頁內容



            for i in range(len(urlLt)):             #依照urlLt陣列裡有多少url就跑幾次
                response = requests.get(urlLt[i])

                tree = etree.HTML(response.text)
                fileName = './' + 'politics' + '/content/'+"news"+urlLt[i].split("_")[-1].replace("/","_")+".txt"  #抓到url裡的內容
                print "999"
                print fileName
                self.writeTxt(fileName,response.content, 'w')     #存檔案



                print urlLt[i]




    def getParsedContent(self, board, sinceDate='a', move='n'):

        self.writeTxt('%s.txt' %(self.logName), datetime.now().strftime('%Y%m%d_%H%M%S_') + board + '_Status: parsing_start') #存成txt檔 查看使用狀態(檢查用)


        fileDir = os.getcwd() + '/' + board + '/content/'   #路徑
        destDir = fileDir.replace('content','saved')

        fileLt = os.listdir(fileDir)



        jsonDict = {}
        for i in fileLt:                        #路徑裡有多少txt就跑幾次
            try:
                jsonDict[re.sub('.txt?','',i)] = self.parseContent(i, board)   #跑parsecontent函式 寫進json
                print jsonDict
            except Exception, e:
                print 'Error: %s - %s' %(i, e)
                self.writeTxt('%s.txt' %(self.logName), datetime.now().strftime('%Y%m%d_%H%M%S_') + i + '_Status: ' + str(e))


        with open(self.logName.replace('crawler','') + board + '.json', 'w') as j:
            json.dump(jsonDict, j, ensure_ascii=False, encoding='utf8')



    def parseContent(self, fileName, board):
        fileContent = codecs.open('./' + board + '/content/' + fileName, 'r', "utf-8").read()   #讀路徑上的檔案
        tree = etree.HTML(fileContent)

        sourceType = 'news'                                             #寫進json的格式
        sourceWebsite = 'CNTV'
        sourceBoard = board


        author = tree.xpath('//span[@class="editor"]')[0].text          #一一從txt檔裡找資料
        print author
        title = tree.xpath('//h1[@id="title"]')[0].text
        print title
        cDate = self.currentDateObject = tree.xpath('//span[@class="time"]')[0].text
        print cDate

        contentElement = tree.xpath('//div[@class="article"]/p')
        print 999999999999999999999999
        #print contentElement
        ##articleContent = tree.xpath('//div[@class="txt"]')[2].text
        articleContent = '\n'.join([i.xpath("normalize-space()") for i in contentElement  if i!= ''])
        #print articleContent


        quoteFrom = ''
        pushIDArray = []
        pushContentArray = []
        pushTimeArray = []
        messageNum = ''
        pushNum = ''

        pageDict = OrderedDict([
        ('sourceType', sourceType),
        ('sourceWebsite', sourceWebsite),
        ('sourceBoard', sourceBoard),
        ('author', author),
        ('title', title),
        ('cDate', cDate),
        ('content', articleContent),
        ('quoteFrom', quoteFrom),
        ('pushIDArray', pushIDArray),
        ('pushContentArray', pushContentArray),
        ('pushTimeArray', pushTimeArray),
        ('messageNum', messageNum),
        ('pushNum', pushNum)
        ])


        return pageDict                 #回傳陣列



urlLt=[]    #陣列 存第一頁所要的所有url
url = 'http://www.news.cn/fortune/'
board = "politics"    #版別跟資料路徑
test().getlink(url)   #取得第一頁所要的所有url
print urlLt


fileDir = os.getcwd() + '/' + board + '/content/'  #儲存所有txt的路徑  getparsedcontent要用到
fileLt = os.listdir(fileDir)

test().getcontent()   #取得網頁內容

reload(sys)
sys.setdefaultencoding('utf-8')


test().getParsedContent(board)  #找尋所有儲存的txt再進行分析出json





