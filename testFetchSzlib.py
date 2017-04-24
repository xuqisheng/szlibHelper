#!/usr/bin/env python
#-*-coding=utf-8-*-

import urllib
import urllib2
import cookielib
import md5

## fake as a normal browser
userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"

szLibRefere = "http://www.szlib.org.cn/MyLibrary/Reader-Access.jsp"

#szLibLogin = "http://www.szlib.org.cn/MyLibrary/readerLoginM.jsp"
szLibLogin = "https://www.jiangfuqiang.cn/MyLibrary/readerLoginM.jsp"

acceptHtml = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"

headersForReqHtml = {"User-Agent": userAgent, "Referer": szLibRefere, "Accept": acceptHtml}

#getLoanListUrl = "http://www.szlib.org.cn/MyLibrary/getloanlist.jsp?readerno=1961683"
getLoanListUrl = "https://www.jiangfuqiang.cn/MyLibrary/getloanlist.jsp?readerno=1961683"

def crawlPage(hrefUrl, deepth, referer):
    pass

#def getNetwordData(url, download_timeout = 5, postDataDict = None, headers = None):
#    data = ""
#    postData = None
#    if postDataDict:
#        postData = urllib.urlencode(postDataDict)
#    print postData
#    # error may happen when opening the url
#    request = urllib2.Request(url, postData, headers)
#    try:
#        response = urllib2.urlopen(request, timeout = download_timeout)
#        data = response.read()
#    except urllib2.HTTPError, e:
#        print e.code, e.reason
#    except urllib2.URLError, e:
#        print e.reason
#    except Exception, e:
#        print "Unexpected error:", e
#    return data
#
def setUpCookie(cookieFileName = ""):
    cookie = None
    if len(cookieFileName) > 0:
        cookie = cookielib.MozillaCookieJar(cookieFileName)
    else:
        cookie = cookielib.CookieJar()
    cookieProcessor = urllib2.HTTPCookieProcessor(cookie)
    cookieOpener = urllib2.build_opener(cookieProcessor)
    urllib2.install_opener(cookieOpener)
    return cookie

def getNetwordData(url, download_timeout = 5, postDataDict = None, headers = None):
    data = ""
    postData = None
    if postDataDict:
        postData = urllib.urlencode(postDataDict)
    print postData
    # error may happen when opening the url
    print "headers:", headers
    request = urllib2.Request(url, postData, headers)
    try:
        response = urllib2.urlopen(request, timeout = download_timeout)
        data = response.read()
    except Exception, e:
        print "Unexpected error:", e
    return data

def getRecordnoFromCookie(cookie):

    return recordno
	
if __name__ == "__main__":

    #cookie = setUpCookie()

    account = "0440050867306"
    password = "19911213"
    pwd_md5 = md5.new(password).hexdigest()
    print "pwd_md5: %s" % (pwd_md5)
    postData = {"username":account, "password": pwd_md5}

    rawHtml = getNetwordData(szLibLogin, 10, postData, headersForReqHtml)

    print "request sent!"
    print "%s" % rawHtml

    #bkListUrl = getLoanListUrl
    #bookList = getNetwordData(bkListUrl, 10, None, headersForReqHtml)

    #print bookList

    #print cookie

