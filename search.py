#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
这里面实现了多个音乐平台的下载功能，主要是为了避免一个平台出现问题就挂掉了
下面依次实现了百度音乐等的下载接口
"""
import sys,os,re
import urllib,urllib2
from bs4 import BeautifulSoup
import json
from multiprocessing import Process
from threading import Timer
import time

#=========================百度音乐下载类=======================================
class BaiDuMusic():
    def __init__(self):
        reload(sys)  
        sys.setdefaultencoding('utf8')   
#     #下载进度
    def cbk(self,a, b, c):  
        try:
            per = 100.0 * a * b / c
            if per > 100:
                per = 100
            self.obj.setValue(per)
        except Exception, e:
            self.obj.setValue(100)
       

    def search(self,songName):
        firstUrl = "http://music.baidu.com/search?key="+urllib.quote(str(songName))
        # print firstUrl
        userAgent = " User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 "
        headers = { 'User-Agent' : userAgent }
        requst = urllib2.Request(firstUrl,headers = headers) 
        result = urllib2.urlopen(requst).read()

        #使用BeautifulSoup快速解析html文档
        soup = BeautifulSoup(result,from_encoding="utf-8")
        res_arr = []
        try:
            tmpjson = soup.find_all("li", { "class" : "bb-dotimg clearfix song-item-hook " })
            for x in tmpjson:
                tmpobj = json.loads(x['data-songitem'])
                value = unicode(tmpobj['songItem']['oid'])+"+++"+unicode(tmpobj['songItem']['author'])+"+++"+unicode(tmpobj['songItem']['sname'])[4:-5]
                res_arr.append(value)
            # for x in res_arr:
                # print x
            return res_arr
        except Exception, e:
            print u"抱歉没有找到相关资源".encode("utf-8")
            return 0
    def download(self,songid,songName,obj,savePath="down/"):
        songpath = open("local.py","r").read().split("+++")[0]
        if songpath != "":
            # print songpath
            savePath = songpath+"/"
        self.obj = obj
        songNewUrl = "http://music.baidu.com/data/music/file?link=&song_id="+str(songid)
        print songNewUrl
        if not os.path.isdir(savePath): 
            os.makedirs(savePath)
        savemp3 = savePath.decode('utf-8')+songName.decode('utf-8')+u".mp3"
        urllib.urlretrieve(songNewUrl, savemp3,self.cbk) 
        # self.down_id = os.getpid()
        # Timer(5,self.delayrun).start() 
    # 限制这个进程执行时间，避免各种原因变成僵尸进程
    # def delayrun(self):
        # print self.down_id
        # return
# =================通过歌名搜索歌曲专辑图======================

class songPic:
    def __init__(self,songName):
        self.songName = songName
        self.begin()
    def begin(self):
        pass

    
if __name__=='__main__':

    bMusic = BaiDuMusic()
    bMusic.search(u"冰 雨")
    # Process(target=bMusic.download, args=(18329670,"冰雨")).start()

    # Process(target=bMusic.search, args=(u"月亮之上".encode('utf-8'),u'music/'.encode('utf-8'))).start()
    # Process(target=bMusic.search, args=(u"匆匆那年".encode('utf-8'),u'music/'.encode('utf-8'))).start()


#测试过程中遇到一些编码上的问题(其实在linux上编码问题很少，主要是window上很多编码问题);
# 这篇文章写得很好,看完过后对python的编码茅塞顿开：
# http://www.cnblogs.com/huxi/archive/2010/12/05/1897271.html
