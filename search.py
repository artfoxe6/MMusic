#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys,os
import urllib,urllib2
from bs4 import BeautifulSoup
import json
from multiprocessing import Process

class BaiDuMusic():
    def __init__(self):
        reload(sys)  
        sys.setdefaultencoding('utf8')   

    def search(self,songName):
        firstUrl = "http://music.baidu.com/search?key="+urllib.quote(str(songName))
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
            return res_arr
        except Exception, e:
            print u"抱歉没有找到相关资源".encode("utf-8")
            return 0
    def download(self,songid,songName,savePath="down/"):
        songNewUrl = "http://music.baidu.com/data/music/file?link=&song_id="+str(songid)
        if not os.path.isdir(savePath):	
        	os.makedirs(savePath)
        savemp3 = savePath.decode('utf-8')+songName.decode('utf-8')+u".mp3"
        urllib.urlretrieve(songNewUrl, savemp3) 
 
if __name__=='__main__':

    bMusic = BaiDuMusic()
    res = bMusic.search(u"冰 雨")
    # for x in res: 
        # print x
    # 1128053+++刘德华+++冰雨
    # 7327899+++李翊君+++冰雨
    # 53535187+++张恒+++冰雨
    Process(target=bMusic.download, args=(1128053,"刘德华-冰雨")).start()
    Process(target=bMusic.download, args=(7327899,"李翊君-冰雨")).start()
    Process(target=bMusic.download, args=(53535187,"张恒-冰雨")).start()


