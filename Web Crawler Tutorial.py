#!python2.7
# -*- coding: utf-8 -*-
#-----------------------------
# Class: 淡江大學 爬蟲教育訓練
# Date: 2015.Sep.02
# Speaker: 洪立全
#
# Note:
#       1. 環境:
#           Python 2.7.9
#           requests 2.7.0
#           lxml 3.4.4
#           selenium 2.45.0
#       2. Python下載網址: https://www.python.org/downloads/release/python-2710/
#       3. 套件安裝方式
#           在cmd下輸入 pip install <package name>
#           安裝指定版本 pip install <package name>==<version number>
#-----------------------------

# I. Python基本操作

# list
##建立list
l = [1, 2, 3]

##呼叫資料
print l[0]
print l[1]
print l[-1]

##增加元素
l.append(4)
print l

##刪除元素
l.remove(4) ##remove(元素名稱)
print l

del l[-1] ##del list[元素位置]
print l


# dictionary
##建立字典
d = {'student1': 'Mike',
    'student2': 'Richard'}

##呼叫資料
print d['student1']
print d['student2']

##增加元素
d.update({'student3': 'Joe'})
print d

##刪除元素
del d['student1']
print d

## 查看所有key值
print d.keys()

## 查看所有value值
print d.values()

## 查看所有元素 以list傳回
print d.items()


# if
x = 0
if x < 0:
    print 'Negative'
elif x > 0:
    print 'Positive'
else:
    print 'Other Number'


# for loop
for i in [1,2,3]:
    print i


# while loop
i = 1
while i <= 10:
    print i
    i+=1


# def
def sum(a, b):
    return a+b

print sum(1,2)

# string
name = 'Josh'
print name[0]
print name[-1]


# II. 網路爬蟲 - 基礎

# get
##以"自由時報"為例

import requests
url = 'http://news.ltn.com.tw/list/politics'
response = requests.get(url)

print response.status_code ##檢查HTTP狀態碼
print response.text

##解析內文
from lxml import etree

tree = etree.HTML(response.text)

tree.xpath('//ul[@id="newslistul"]/li/a') ##list of Elements
print tree.xpath('//ul[@id="newslistul"]/li/a') ##回傳為list型態
print tree.xpath('//ul[@id="newslistul"]/li/a')[0].text ##查看元素內文字

searchResult = tree.xpath('//ul[@id="newslistul"]/li/a')
for i in searchResult: ##查看searchResult內每個Element的文字是否為我們需要
    print i.text

print tree.xpath('//ul[@id="newslistul"]/li/a')[0].get('href') ##查看Elements內的attribute
searchResult = tree.xpath('//ul[@id="newslistul"]/li/a')
for i in searchResult:
    print i.get('href')

urlLt = []
for i in searchResult:
    urlLt.append(i.get('href')) ##將結果存入urlLt
print urlLt

##補充
'http://news.ltn.com.tw/news/politics/breakingnews/1460751'
urlLt2 = map(lambda i: 'http://news.tln.com'+i, urlLt)
print urlLt2

urlLt3 = ['http://news.tln.com%s' %(i.get('href')) for i in searchResult]
print urlLt3


# selenium
##以"台灣大哥大"為例

from selenium import webdriver
driver = webdriver.Firefox()
driver.get('https://www.google.com.tw') ##瀏覽網頁

url = 'http://www.taiwanmobile.com/cs/public/storeAction.do?utm_source=service&utm_medium=localnav&utm_campaign=location'
driver.get(url)

driver.find_elements_by_xpath('//select[@name="zip_county"]/option') ##檢查是否抓到欲抓取元素
print driver.find_elements_by_xpath('//select[@name="zip_county"]/option')[1].get_attribute('value') ##查看

driver.find_elements_by_xpath('//select[@name="zip_county"]/option')[1].click() ##點選下拉選單的"基隆市"

print driver.find_elements_by_xpath('//a[@id="queryButton"]')[0].text ##尋找"查詢"按鈕
driver.find_elements_by_xpath('//a[@id="queryButton"]')[0].click() ##模擬滑鼠點擊


# post
##以"蘋果日報 搜尋"為例
payloads = {'searchMode': 'Adv',
            'searchType': 'text',
            'querystrA': '汽車',
            'select': 'AND',
            'sdate': '2003-05-02',
            'edate': '2015-10-02'}

response = requests.post(url = 'http://search.appledaily.com.tw/appledaily/search', data = payloads) ##模擬Form Data傳入參數
print response.text


# III. 網路爬蟲 - 進階技巧

# split
print 'http://www.mobile01.com/newsdetail.php?id=17411'.split('?') ##字串split後為list型態

id = 'http://www.mobile01.com/newsdetail.php?id=17411'.split('?')[-1]
print id

# replace
print 'http://www.mobile01.com/newsdetail.php?id=17411'.replace('http://www.mobile01.com/','')

# re.sub
import re
print re.sub('.*id=','', 'http://www.mobile01.com/newsdetail.php?id=17411')

# datetime
from datetime import datetime

datetime.strptime('20151001', '%Y%m%d')
print datetime.strptime('20151001', '%Y%m%d').strftime('%Y')
print datetime.strptime('20151001', '%Y%m%d').strftime('%Y-%m-%d')
##Reference: https://docs.python.org/2/library/datetime.html

# string formatting
print 'My name is %s, and my gender is %s.' %('Josh', 'male')

print 'My name is %(name)s, and my gender is %(gender)s.' %({'name':'Josh', 'gender': 'male'})


# class寫法
class me:
    def __init__(self):
        self.name = 'Josh'
        self.gender = 'male'

    def getInfo(self):
        print 'My name is %s, and my gender is %s.' %(self.name, self.gender)

me().getInfo()
print me().name
print me().gender


class personalInfo:
    def __init__(self, name, gender): ##實體化時給予變數
        self.name = name
        self.gender = gender

    def getInfo(self):
        print 'My name is %s, and my gender is %s.' %(self.name, self.gender)

personalInfo('John','male').getInfo()
personalInfo('Mary','female').getInfo()


class personalInfo2:
    def __init__(self):
        self.name = 'Josh'
        self.gender = 'male'

    def getInfo(self, name, gender): ##在方法中給變數
        print 'My name is %s, and my gender is %s.' %(name, gender)

personalInfo2().getInfo('Susan','female')
print personalInfo2().name
print personalInfo2().gender