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

reload(sys)
sys.setdefaultencoding('utf-8')


boardNumDict = {'TRAVEL':'p4.php?seriesa=1&page=',
'FOOD':'p4.php?seriesa=2&page=',
'LIVE':'p4.php?seriesa=3&page=',
'ENTERTAINMENT':'p4.php?seriesa=5&page=',
'DIGITAL':'p4.php?seriesa=6&page=',
'ART':'p4.php?seriesa=4&page='}



class tpw:
	def __init__(self):
		self.name = 'TaipeiWalker'
		self.logName = 'TPW_crawler'

	def writeTxt(self, fileName, content, method='a'):
		file = open(fileName,method)
		file.write(content + '\n')
		file.close()
	##目錄頁連結及抓取內文網址
	def getBoardContent(self, board, endDate):
		page = 1
		self.writeTxt('%s.txt' %(self.logName
        ), datetime.now().strftime('%Y%m%d_%H%M%S_') + '_Status: crawler_start')
		fileDir = os.getcwd() + '/' + board + '/page_content/'
		print fileDir
		fileLt = [i.replace('.txt','') for i in os.listdir(fileDir)]
		endDateObject = datetime.strptime(endDate,'%Y-%m-%d')
		currentDateObject = datetime.now()

		while currentDateObject >= endDateObject:
			url = 'http://www.taipeiwalker.com.tw/%(board)s%(page)s' % {'board':(boardNumDict[board]),'page':page}
			print 'Get: %s' %(url)
			try:
				response = requests.get(url)
				self.writeTxt('./%(board)s/%(logName)s_%(board)s.txt' %{'board':board,'logName':self.logName}, datetime.now().strftime('%Y%m%d_%H%M%S_') + url + '_Status:' + str(response.status_code))
			except Exception, e:
				self.writeTxt('./%(board)s/%(logName)s_%(board)s.txt' %{'board':board,'logName':self.logName}, datetime.now().strftime('%Y%m%d_%H%M%S_') + url + '_Status:' + str(e))
				print 'Error: %s' %(e)
			if response.ok:
				try:
					tree = etree.HTML(response.content)
					urlElement = tree.xpath('//div[@class="title"]/a')
					destURLLt = ['http://www.taipeiwalker.com.tw/%s' %(i.get('href')) for i in urlElement]
					random.shuffle(destURLLt)
					##內文網址
					for i in destURLLt:
						if i.split("tw/")[-1].replace("?","_") not in fileLt:
							self.getPageContent(i, board)
							time.sleep(random.randint(1,3))
				except UnicodeError,e:
					print 'UnicodeError Error:%s' % (e)
			try:
				datestr = tree.xpath('//div[@class="time"]')[-1].text.replace(u'\u767C\u8868\u65E5\u671F\uFF1A',"").replace(u'\u3000',"").replace("/","-").encode('utf-8')
				currentDateObject = datetime.strptime(datestr, '%Y-%m-%d')
			except:
				currentDateObject = datetime.now()
			page+=1
			self.writeTxt('./%(board)s/%(logName)s_%(board)s.txt' %{'board':board,'logName':self.logName},'\r\nNEXT_PAGE')
		self.writeTxt('%s.txt' %(self.logName), datetime.now().strftime('%Y%m%d_%H%M%S_') + board + '_Status: crawler_complete')

	##開啟抓取下來的檔案，及寫入json
	def getParsedContent(self, board, sinceDate='a', move='n'):
		self.writeTxt('%s.txt' %(self.logName), datetime.now().strftime('%Y%m%d_%H%M%S_') + board + '_Status: parsing_start')
		fileDir = os.getcwd() + '/' + board + '/page_content/'
		destDir = fileDir.replace('page_content','saved')
		fileLt = os.listdir(fileDir)

		##取得page_content指定日期以前的檔案
		if sinceDate != 'a':
			sinceDateObject = datetime.strptime(sinceDate, '%Y-%m-%d')
			fileLt = [i for i in fileLt if datetime.fromtimestamp(os.path.getctime(fileDir + i)) >= sinceDateObject]

		jsonDict = {}
		for i in fileLt:
			try:
				##.sub(想要取代的字串,取代後的字串) 放入jsonDICT
				jsonDict[re.sub('.txt?','',i)] = self.parseContent(i, board)
			except Exception, e:
				print 'Error: %s - %s' %(i, e)
				self.writeTxt('%s.txt' %(self.logName), datetime.now().strftime('%Y%m%d_%H%M%S_') + i + '_Status: ' + str(e))

            ##把檔案從page_content搬到saved
			if move == 'y':
				shutil.move(fileDir + i, destDir + i)

		with open(self.logName.replace('crawler','') + board + '.json', 'w') as j:
			json.dump(jsonDict, j, ensure_ascii=False, encoding='utf-8')
		##json存檔
		self.writeTxt('%s.txt' %(self.logName), datetime.now().strftime('%Y%m%d_%H%M%S_') + board + '_Status: parsing_complete')


	##抓取內文
	def getPageContent(self, url, board):
		print 'Get: %s' %(url)
		try:
			response = requests.get(url)
			self.writeTxt('./%(board)s/%(logName)s_%(board)s.txt' %{'board':board,'logName':self.logName}, datetime.now().strftime('%Y%m%d_%H%M%S_') + url + '_Status:' + str(response.status_code))
		except Exception, e:
			self.writeTxt('./%(board)s/%(logName)s_%(board)s.txt' %{'board':board,'logName':self.logName}, datetime.now().strftime('%Y%m%d_%H%M%S_') + url + '_Status:' + str(e))
			print 'Error: %s' %(e)

		if response.ok:
			tree = etree.HTML(response.content)
			urlElement = tree.xpath('//div[@id="inside1"]')
			articleContent = ''.join([i.xpath("normalize-space()") for i in urlElement])
			if u'\u7121\u6b64\u5247\u65b0\u805e' not in articleContent: ##"無此則新聞"
				fileName = '.\\' + board + '\\page_content\\' + url.split(".tw/")[-1].replace("?","_").replace("/","_")+".txt"
				self.writeTxt(fileName, response.content, 'w')

##將檔案內容寫成dict並回傳給getParsedContent製作成json
	def parseContent(self, fileName, board):
		fileContent = codecs.open('./'+board+'/page_content/'+fileName, 'r', "utf-8").read()
		print fileContent
		tree = etree.HTML(fileContent)
		sourceType = 'news'
		sourceWebsite = 'TaipeiWalker'
		sourceBoard = board
		url = 'http://www.taipeiwalker.com.tw/%s' %(fileName.replace("_",'?').replace('.txt',''))
		author = u'\u7121\u4f5c\u8005'
		title = tree.xpath('//div[@class="p4title"]')[0].text
		cTimeObject = tree.xpath('//div[@class="p4time"]')[0].text.replace(u'\u767C\u8868\u65E5\u671F\uFF1A',"").replace(u'\u3000',"").replace("/","")
		if u'\u4f5c\u8005\uff1a' in cTimeObject:
			author = cTimeObject.split(u'\u4f5c\u8005\uff1a')[1]
			cTimeObject = cTimeObject.split(u'\u4f5c\u8005\uff1a')[0]
		cTimeObject = '%s_00:00' %(cTimeObject) if '_' not in cTimeObject else cTimeObject
		cDate = cTimeObject.split('_')[0]
		cTime = cTimeObject.split('_')[1]
		contentElement = tree.xpath('//span[@style="font-size: small;"]')
		print contentElement
		articleContent = ''.join([i.xpath("normalize-space()") for i in contentElement if i!= ''])
		print articleContent
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
		('url', url),
		('author', author),
		('title', title),
		('cTimeObject', cTimeObject),
		('cDate', cDate),
		('cTime', cTime),
		('content', articleContent),
		('quoteFrom', quoteFrom),
		('pushIDArray', pushIDArray),
		('pushContentArray', pushContentArray),
		('pushTimeArray', pushTimeArray),
		('messageNum', messageNum),
		('pushNum', pushNum)
		])
		return pageDict



board = 'TRAVEL' #版別
endDate = '2015-08-17' #結束日期
tpw().getBoardContent(board,endDate)
#time.sleep(random.randint(1,3))
tpw().getParsedContent(board,endDate)
#print tpw().parseContent('p4-detail.php_id=2742.txt',board)



