#!/usr/bin/env python
#-*-coding=utf-8-*-

import urllib
import urllib2
import cookielib
import md5
import requests
import xml.etree.cElementTree as ET
import json
import re

## fake as a normal browser
userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
szLibRefere = "http://www.szlib.org.cn/MyLibrary/Reader-Access.jsp"
acceptHtml = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headersForReqHtml = {"User-Agent": userAgent, "Referer": szLibRefere, "Accept": acceptHtml}

szLibLogin = "http://www.szlib.org.cn/MyLibrary/readerLoginM.jsp"
generalGetLoanListUrl = "http://www.szlib.org.cn/MyLibrary/getloanlist.jsp?readerno=%s"
generalRenewUrl = "http://www.szlib.org.cn/MyLibrary/response.jsp?v_select=%s&"


# for test
getLoanListUrl = "http://www.szlib.org.cn/MyLibrary/getloanlist.jsp?readerno=1961683"

# utils
def log(logString):
    print logString
    # write to log file

def parseXmlToJsonString(xmlString):
    loanlist = list()
    root = ET.fromstring(xmlString)
    infolistNodes = root.find("loanlist").findall("meta")
    for infolistNode in infolistNodes:
        bookInfoDict = dict()
        for node in infolistNode.iter():
            #print node.tag, node.text
            if node.text is None:
                bookInfoDict[node.tag] = ""
            else:
                bookInfoDict[node.tag] = node.text
        loanlist.append(bookInfoDict)
        #print ""
    #print loanlist
    jsonString = json.dumps(loanlist)
    return jsonString

def parseReturnDate(xmlString):
    tt = re.findall(".*(20[0-9]{6})", xmlString)
    if len(tt) > 0:
        return tt[0]
    else:
        return ""

def getValFromCookie(cookie, attrName):
    for item in cookie:
        if item.name == attrName:
            return item.value
    return None

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
    #print postData
    #print "headers:", headers
    # error may happen when opening the url
    request = urllib2.Request(url, postData, headers)
    try:
        response = urllib2.urlopen(request, timeout = download_timeout)
        data = response.read()
    except Exception, e:
        print "Unexpected error:", e
    return data

class LoanInfoDef:
    " detail about loan info "

    def __init__(self):
        pass
    def parseXmlInfo(xmlString):
        pass

class UserInfoDef:
    " detail about libary user "

    def __init__(self, accountName, pwdMd5):
        self.account = accountName
        self.pwdMd5 = pwdMd5
        self.hasLogin = False
        self.httpConn = None
        self.cookie = None
        self.loanList = list()
        # most familiar way: use urlib2
        self.opener = None

    def mlog(self, logStr):
        logRecord = "%s: %s" % (self.account, logStr)
        log(logRecord)

    def sendFailed(self, handler, code, content):
        handler.send_error(code, content)

    def sendSuccess(self, handler, content):
        handler.send_response(200) 
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(content)

    def handleRequest(self, postData, handler):
        operation = postData.get("operation")
        if operation is None or operation == "login":
            if self.toLogin(handler):
                self.sendSuccess(handler, "Login success!")
                return
        elif operation == "getLoanList":
            if self.hasLogin == False:
                if self.toLogin(handler) == False:
                    self.sendFailed(handler, 404, "login to szlib failed!")
                    return
            # to fetch loan list
            self.toGetLoanList(handler)
        elif operation == "reNewBook":
            barcode = postData.get("barcode")
            if barcode is None or len(barcode) <= 0:
                self.sendFailed(handler, 400, "barcode is empty!");
                return
            if self.hasLogin == False:
                if self.toLogin(handler) == False:
                    self.sendFailed(handler, 404, "login to szlib failed!")
                    return
            # to renew book
            self.toRenewBook(handler, barcode)

    def setUpCookieAndOpener(self):
        self.cookie = cookielib.CookieJar()
        cookieProcessor = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(cookieProcessor)

    def getNetwordData(self, url, download_timeout=5, postDataDict=None, headers=None):
        if self.opener is None:
            self.mlog("opener is None!")
            return False
        data = ""
        postData = None
        if postDataDict:
            postData = urllib.urlencode(postDataDict)
        #print postData
        #print "headers:", headers

        request = urllib2.Request(url, postData, headers)
        try:
            response = self.opener.open(request, timeout = download_timeout)
            data = response.read()
        except Exception, e:
            self.mlog("Unexpected error: %s" % str(e))
        return data

    def toLogin(self, handler):
        self.setUpCookieAndOpener();
        postDataDict = {"username":self.account, "password": self.pwdMd5}
        return self.getNetwordData(szLibLogin, 5, postDataDict, headersForReqHtml)

    def toGetLoanList(self, handler):
        if self.cookie is None:
            self.sendFailed(handler, 404, "cookie is None!")
            return

        recordno = getValFromCookie(self.cookie, "recordno")
        if recordno is None:
            self.sendFailed(handler, 404, "recordno in cookie is None!")
            return
        self.mlog("recordno: %s" % recordno)
        loanListUrl = generalGetLoanListUrl % recordno
        self.mlog("loadListUrl: %s" % loanListUrl)

        loanListReferer = "http://www.szlib.org.cn/MyLibrary/Loan-Status.jsp"
        headersForReqHtml["Referer"] = loanListReferer

        data = self.getNetwordData(loanListUrl, 8, None, headersForReqHtml)
        if data == False:
            self.sendFailed(handler, "404", "fetch loan list failed!")
        else:
            # parse data to json
            jsonString = parseXmlToJsonString(data)
            self.sendSuccess(handler, jsonString)

    def toRenewBook(self, handler, barcode):
        if self.cookie is None:
            self.sendFailed(handler, 404, "cookie is None!")
            return
        renewUrl = generalRenewUrl % barcode
        self.mlog("renewUrl: %s" % renewUrl)

        renewReferer = "http://www.szlib.org.cn/MyLibrary/Loan-Status.jsp"
        headersForReqHtml["Referer"] = renewReferer

        data = self.getNetwordData(renewUrl, 8, dict(), headersForReqHtml)
        if data:
            returnDate = parseReturnDate(data)
            respStr = '{"returndate":"%s"}' % returnDate
            self.sendSuccess(handler, respStr)
            self.mlog("renew succeed, return: %s" % respStr)
        else:
            self.sendFailed(handler, 404, "renew %s failed!" % barcode)
            self.mlog("renew failed!")

    def login(self):
        postData = {"username":self.account, "password": self.pwdMd5}
        try:
            req = requests.post(szLibLogin, data=postData, headers=headersForReqHtml)
            if (req.status_code == 200):
                self.cookie = req.cookie
                self.hasLogin = True
                return True
        except ConnectionError, e:
            self.mlog("login, failed to connet to server")
        except Timeout, e:
            self.mlog("login, time out")
        except HTTPError, e:
            self.mlog("login, response status is not 200: %s" % self.status_code)
        except request.exception.RequestException, e:
            self.mlog("login, unknow error:" + str(e))
        return False

    def fetchLoanList(self):
        urlParam = {"readerno":self.getReaderno()}
        req = request.get(getLoanListUrl, params=urlParam)
        print req.text
        pass

    def renewBook(self, loanInfo):
        pass

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

    #bookList = getNetwordData(getLoanListUrl, 10, None, headersForReqHtml)
    #print bookList

    #print cookie

