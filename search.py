#!/usr/bin/env python
#coding=utf-8
"""
这里面实现了多个音乐平台的下载功能，主要是为了避免一个平台出现问题就挂掉了
下面依次实现了百度音乐等的下载接口
"""
import sys,os,re
import urllib,urllib2
from bs4 import BeautifulSoup
import json
#=========================百度音乐下载类=======================================
class BaiDuMusic():
    def __init__(self,songName,musicDir):
        reload(sys)  
        sys.setdefaultencoding('utf8')   
        self.songName = songName
        self.musicDir = musicDir
        pass
    #下载进度
    def cbk(self,a, b, c):  
		per = 100.0 * a * b / c
		if per > 100:
			per = 100
		print '%.2f%%' % per ,

    def search(self):
        firstUrl = "http://music.baidu.com/search?key="+self.songName 
        userAgent = " User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 "
        headers = { 'User-Agent' : userAgent }
        requst = urllib2.Request(firstUrl,headers = headers) 
        result = urllib2.urlopen(requst).read()
        #使用BeautifulSoup快速解析html文档
        soup = BeautifulSoup(result,from_encoding="utf-8")
        tmpjson = soup.find(id='first_song_li')['data-songitem']
        #json字符串转dict类型
        tmpobj = json.loads(tmpjson)
        #歌曲的oid标示符
        oid = tmpobj['songItem']['oid']
        if not oid:
        	print u"抱歉没有找到相关资源"
        	return False
        songNewUrl = "http://music.baidu.com/data/music/file?link=&song_id="+str(oid)
        if not os.path.isdir(self.musicDir):	
        	os.makedirs(self.musicDir)
        urllib.urlretrieve(songNewUrl, self.musicDir+self.songName+".mp3",self.cbk) 
        print self.songName+u".mp3下载完成..."

    

if __name__=='__main__':
    bMusic = BaiDuMusic(u"冰雨",'music/')
    bMusic.search()
