# !/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import json
import MySQLdb
import re
import sys
import time
import random
from time import mktime, strptime

reload(sys)
sys.setdefaultencoding("utf-8")


def int_time(sj):
    sj_int = int(mktime(strptime(sj, '%Y-%m-%d %H:%M:%S')))
    return sj_int


def get_article_url():
    url = urllib2.urlopen("http://uzone.univs.cn/blog/2654701.html")
    rawdata = url.read()
    a2 = []
    a3 = []
    soup = BeautifulSoup(rawdata, "html.parser")
    for a in soup.findAll('a', href=True):
        if re.findall('blog_2654701', a['href']):
            a1 = a['href']
            a2.append(a1)
    for b in range(0, len(a2), 3):
        a3.append(a2[b])
    return a3


def get_content():
    urls = get_article_url()
    for c in range(0, 10):
        mon = time.strftime('%m', time.localtime(time.time()))
        year = time.strftime('%Y', time.localtime(time.time())).strip("20")
        day = time.strftime('%d', time.localtime(time.time()))
        hour = time.strftime('%H', time.localtime(time.time()))
        sec = time.strftime('%S', time.localtime(time.time()))
        min = time.strftime('%M', time.localtime(time.time()))
        Nowaday = str(year)+"-"+str(mon)+"-"+str(day)
        Nowaday1 = "20"+str(year)+"-"+str(mon)+"-"+str(day)+" "+str(hour)+":"+str(min)+":"+str(sec)
        url = urllib2.urlopen("http://uzone.univs.cn/blog/" + urls[c])
        url_json = json.dumps("http://uzone.univs.cn/blog/" + urls[c])
        soup = BeautifulSoup(url.read(), "html.parser")
        tm = soup.title.string
        tm_json = json.dumps(tm)
        zw = soup.find(id="xspace-showmessage").contents
        zw_json = json.dumps(str(zw))
        sj = soup.find(class_="xspace-smalltxt").get_text()
        sj1 = re.search(r"\d+-\d+-\d+\s\d+:\d+:\d+", str(sj))
        sj_now = "20"+sj1.group()
        sj_test = re.search(r"\d+-\d+-\d+", str(sj)).group()
        if sj_test != Nowaday:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='你的密码', db='你的数据库', charset='utf8')
           # cursor.execute("""create database if not exists 你的数据库名""")
           # conn.select_db('你的数据库名')
           # cursor.execute("""create table if not exists cai_article(author int, `time` int, edittime int, eidtor char(100), `from` char(100), fromurl char(100), `type` int, thumb char(100), top int, click int, realclick int, title char(100), content text)""")
            num1 = random.randrange(100, 200)
            cursor = conn.cursor()
            cursor.execute("select uid from user where realname='测试账号'")
            uid = re.search(r"\d+", str(cursor.fetchall())).group()
            value = (int(uid), int_time(sj_now), int_time(Nowaday1), 'XXXX', 'XXXXXX', "http://uzone.univs.cn/blog/" + urls[c], 0, '0', 0, num1, 0, tm_json, zw_json)
            try:
                cursor.execute("select fromurl from article where fromurl=%s"%url_json)
                result = cursor.fetchall()
                if not result:
                    print "not record"
                # Execute the SQL command
                    cursor.execute("""insert into article(author, `time`, edittime, editor, `from`, fromurl, `type`, thumb, top, click, realclick, title, content) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)""", value)
                # Commit your changes in the database
                    conn.commit()
                    print "inserted"
                else:
                    print "exist"
            except:
                 #Rollback in case there is any error
                print "rollback"
             #disconnect from server
            conn.close()


while 1:
    hour = time.strftime('%H', time.localtime(time.time()))
    sec = time.strftime('%S', time.localtime(time.time()))
    min = time.strftime('%M', time.localtime(time.time()))
    Nowtime = str(hour)+":"+str(min)+":"+str(sec)
    #if min == 54:
    #	print Nowtime
    if Nowtime == "00:55:00":
        print Nowtime
        get_content()
