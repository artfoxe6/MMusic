#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
百度MV接口
"""
import sys,os,re
import urllib,urllib2
from bs4 import BeautifulSoup
# import json
from multiprocessing import Process
# from threading import Timer
import time

#=========================百度音乐下载类=======================================
class BaiDuMV():
    def __init__(self):
        reload(sys)  
        sys.setdefaultencoding('utf8')   
# ----------------------------------------抓取百度mv推荐页---------------------------------------
    def recommend(self):
        try:
            oldtime = open("icon/vars.data","r").read().split("|||")[-1:][0]
            if ( time.time() - float(oldtime) ) < 3600*24:
                return open("icon/vars.data","r").read()
            # print oldtime
        except Exception, e:
            print e
        
        url = "http://music.baidu.com/mv"
        userAgent = " User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 "
        headers = { 'User-Agent' : userAgent }
        requst = urllib2.Request(url,headers = headers) 
        result = urllib2.urlopen(requst).read()

        soup = BeautifulSoup(result,from_encoding="utf-8")  
        try:
            tmpjson = soup.find_all(attrs={"class":"mv-cover  mv-cover-hook"})  #找到模糊的推荐mv
        except Exception, e:
            print u"抱歉没有找到相关资源".encode("utf-8")
            return
        self.url_img_songer = ""
        tmpjson = tmpjson[:10]  #提取正确的推荐mv
        # print tmpjson
        for x in tmpjson:
            url = re.findall(r'<a href=(.*)target', str(x))[0]
            url = "http://music.baidu.com"+str(url[1:-2])
            img = re.findall(r'<img alt=".*"\s+src=(.*)>',str(x))[0]
            img = img[1:-1]
            songer = re.findall(r'<img alt="(.*)"\s+src=',str(x))[0]
            # print str(songer[0]).encode("gbk")
            imgpath = "icon/"+url[-9:]+".jpg"
            self.url_img_songer+=url+"+++"+imgpath+"+++"+str(songer)+"|||"
            # print url
            # ------------把图片保存到icon---------------
            # print url[-6:]
            # Process(target=self.downPic, args=(img,"icon/"+url[-9:]+".jpg")).start()
        # print self.url_img_songer
        open("icon/vars.data","w").write(self.url_img_songer+str(time.time()))
        return self.url_img_songer
# ---------------------------------------用户搜索指定MV------------------------------
    def searchMV(self,songName):
        url = "http://music.baidu.com/search?key="+urllib.quote(songName)
        userAgent = " User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 "
        headers = { 'User-Agent' : userAgent }
        requst = urllib2.Request(url,headers = headers) 
        result = urllib2.urlopen(requst).read()
        
        soup = BeautifulSoup(result,from_encoding="utf-8")  
        try:
            tmpjson = soup.find_all(attrs={"class":"mv-icon"})  #找到所有mv
        except Exception, e:
            print u"抱歉没有找到相关资源".encode("utf-8")
            return
        self.resmv = []
        tmpjson = tmpjson[:4]  #提取前三个mv
        for x in tmpjson:
            url = re.findall(r'href=(.*)target', str(x))[0]
            url = "http://music.baidu.com"+url[1:-2]
            self.resmv.append(url)
        return  self.resmv
    def downPic(self,url,fpath):
            urllib.urlretrieve(url, fpath) 


if __name__=='__main__':

    mv= BaiDuMV()
    mv.recommend()
    # print mv.searchMV("我可以抱你吗")


# 1419572356.4
# 1419572389.21
# 1419572397.7