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
import math

## fake as a normal browser
userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
szLibRefere = "http://www.szlib.org.cn/MyLibrary/Reader-Access.jsp"
acceptHtml = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headersForReqHtml = {"User-Agent": userAgent, "Referer": szLibRefere, "Accept": acceptHtml}

szLibLogin = "http://www.szlib.org.cn/MyLibrary/readerLoginM.jsp"
generalGetLoanListUrl = "http://www.szlib.org.cn/MyLibrary/getloanlist.jsp?readerno=%s"
generalRenewUrl = "http://www.szlib.org.cn/MyLibrary/response.jsp?v_select=%s&"
generalGetLoanHistoryUrl = "http://www.szlib.org.cn/MyLibrary/LoanHistory.jsp?v_StartDate=%s&v_EndDate=%s&v_ServiceAddr=&CardOrBarcode=cardno&cardno=%s&v_LoanType=Ea&curpage=%d"

# for test
getLoanListUrl = "http://www.szlib.org.cn/MyLibrary/getloanlist.jsp?readerno=1961683"

AGENT_NEW_MOBILE = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Mobile Safari/537.36'

URL_NEW_LOGIN = "http://www.szlib.org.cn/szlibmobile/proxyBasic.jsp?http://58.60.2.115:8881/SSBusiness/readermanage/readerLogin?username=%s&password=%s"
URL_NEW_LOANLIST = "http://www.szlib.org.cn/szlibmobile/proxyBasic.jsp?http://58.60.2.115:8881/SSBusiness/circulation/getLoanList?readerno=%s"
URL_NEW_RENEW = "http://www.szlib.org.cn/szlibmobile/proxyBasic.jsp?http://58.60.2.115:8881/SSBusiness/circulation/Renew?barcode=%s&userid=%s&ip=%s"
URL_NEW_READER_INFO = "http://www.szlib.org.cn/szlibmobile/proxyBasic.jsp?http://58.60.2.115:8881/SSBusiness/readermanage/getreaderxmlByIdx?index=cardno&value=%s"
URL_NEW_COVER = "http://202.112.150.126/index.php?client=szlib&isbn=%s/cover"
URL_NEW_PREBOOK_ALL = "http://www.szlib.org.cn/szlibmobile/proxyBasic.jsp?http://58.60.2.115:8881/SSBusiness/requestmanage/getReserveRequest?readerno=%s&requestStatus=all&recordType=Y&v_page=1"

# general setting
G_USER_LIFE_COUNT = 8
G_REQUEST_TIMEOUT = 5

# utils
def log(logString):
    print logString
    # write to log file

def checkLegalISBN(isbn):
    if isbn is None or len(isbn) <= 0:
        return False
    legalSet = set([str(c) for c in range(0, 10)])
    legalSet.add('-')
    #print legalSet
    for c in isbn:
        if c not in legalSet:
            return False;
    return True

def parseLoginRespXml(xmlString):
    if xmlString is None or len(xmlString) == 0:
        return None;
    infoDict = dict();
    root = ET.fromstring(xmlString)
    for node in root:
        if node.text is None:
            infoDict[node.tag] = ""
        else:
            infoDict[node.tag] = node.text
    return infoDict

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

def getHistoryJsonFromXml(xmlString):
    print xmlString
    if xmlString is None or len(xmlString) == 0:
        return "";
    loanlist = list()
    root = ET.fromstring(xmlString)
    # get totalno
    totalno = 0
    totalno_lst = root.findall("totalno")
    if totalno_lst and len(totalno_lst) > 0:
        totalno = int(totalno_lst[0].text)
    infolistNodes = root.findall("record")
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
    #jsonString = json.dumps(loanlist)
    return (loanlist, totalno)

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

def getSzlibBookCover(isbn):
    coverUrl = URL_NEW_COVER % isbn
    headers = {'Accept': 'image/webp,image/*,*/*;q=0.8',
               'User-Agent': AGENT_NEW_MOBILE,
               'Referer': 'http://www.szlib.org.cn/szlibmobile/mylibrary/mem_borrow.html'}
    print "Get Cover: %s" % (coverUrl)
    resp = requests.get(coverUrl, headers=headers, timeout=G_REQUEST_TIMEOUT)
    #print "get cover, req  headers:", resp.request.headers
    #print "get cover, resp headers:", resp.headers
    #print resp.content
    return resp.content

def getReaderInfo(cardno):
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'User-Agent': AGENT_NEW_MOBILE,
               'Referer': 'http://www.szlib.org.cn/szlibmobile/mylibrary/mem_info.html'}
    readerInfoUrl = URL_NEW_READER_INFO % (cardno)
    resp = requests.get(readerInfoUrl, headers=headers, timeout=G_REQUEST_TIMEOUT)
    print "get reader info:", resp.content
    return resp.content

def getReserveBookAll(readerno):
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'User-Agent': AGENT_NEW_MOBILE,
               'Referer': 'http://www.szlib.org.cn/szlibmobile/mylibrary/mem_preborrow.html'}
    reserveBookUrl = URL_NEW_PREBOOK_ALL % (readerno)
    resp = requests.get(reserveBookUrl, headers=headers, timeout=G_REQUEST_TIMEOUT)
    print "get reserve book:", resp.content
    return resp.content

class LoanInfoDef:
    " detail about loan info "

    def __init__(self):
        pass
    def parseXmlInfo(xmlString):
        pass

class UserInfoDef:
    " detail about libary user "

    def __init__(self, accountName):
        self.account = accountName
        self.pwdMd5 = ""
        self.hasLogin = False
        self.httpConn = None
        self.cookie = None
        self.loanList = list()
        # most familiar way: use urlib2
        self.opener = None

        # life count
        self.lifecount = G_USER_LIFE_COUNT
        self.inUsing = 0
        # security
        self.loginFailedCount = 10

    def mlog(self, logStr):
        logRecord = "%s: %s" % (self.account, logStr)
        log(logRecord)

    def sendFailed(self, handler, code, content):
        #handler.send_error(code, content)
        handler.send_response(code) 
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(content)

    def sendSuccess(self, handler, content):
        handler.send_response(200) 
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(content)

    def handleRequest(self, postData, handler):
        operation = postData.get("operation")
        passwdMd5 = postData.get("password")

        if operation is None or operation == "login":
            status, content = self.toLogin(handler, passwdMd5)
            if status:
                self.sendSuccess(handler, content)
                self.pwdMd5 = passwdMd5
                self.hasLogin = True
            else:
                self.sendFailed(handler, 404, content)
                self.hasLogin = False
                self.loginFailedCount -= 1
            return
        elif self.hasLogin == False:
            self.mlog("Do not has login befor doing operation!")
            self.mlog("Will relogin!")
            # try to login
            status, content = self.toLogin(handler, passwdMd5)
            if status:
                self.mlog("relogin failed!")
                self.sendFailed(handler, 404, content)
                self.loginFailedCount -= 1
                return
            else:
                # update password
                self.mlog("relogin success!")
                self.pwdMd5 = passwdMd5
                self.hasLogin = True
            # just continue

        if passwdMd5 != self.pwdMd5:
            self.sendFailed(handler, 404, "login to szlib failed!")
            return

        if operation == "getLoanList":
            # to fetch loan list
            #self.toGetLoanList(handler)
            self.fetchLoanList(handler)
        elif operation == "reNewBook":
            barcode = postData.get("barcode")
            if barcode is None or len(barcode) <= 0:
                self.sendFailed(handler, 400, "barcode is empty!");
                return
            # to renew book
            self.toRenewBook(handler, barcode)
        elif operation == "getReaderInfo":
            cardno = postData.get("cardno")
            if cardno is not None:
                self.sendSuccess(handler, getReaderInfo(cardno))
            else:
                self.sendFailed(handler, 404, "cardno is null!");
        elif operation == "getLoanHistory":
            cardno = postData.get("cardno")
            startdate = postData.get("startdate")
            enddate = postData.get("enddate")
            self.toGetLoanHistory(handler, cardno, startdate, enddate)
        elif operation == "getReserveBook":
            #readerno = postData.get("readerno")
            recordno = getValFromCookie(self.cookie, "recordno")
            self.mlog("readerno: %s" % (recordno))
            self.sendSuccess(handler, getReserveBookAll(recordno))
        elif operation == "logout":
            pass

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

    def toLogin(self, handler, passwdMd5):
        self.setUpCookieAndOpener();
        postDataDict = {"username":self.account, "password": passwdMd5}
        loginResp = self.getNetwordData(szLibLogin, 5, postDataDict, headersForReqHtml)
        infoDict = parseLoginRespXml(loginResp.strip())
        infoJson = json.dumps(infoDict)
        if infoDict["message"] == "OK": 
            #print "login success, info dict:", infoDict
            return True, infoJson
        else:
            print "login failed, info dict:", infoDict["message"]
            return False, infoJson

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
            #self.mlog("loan list: %s" % (jsonString))

    def toRenewBook(self, handler, barcode):
        if self.cookie is None:
            self.sendFailed(handler, 404, "cookie is None!")
            return
        renewUrl = generalRenewUrl % barcode
        self.mlog("renewUrl: %s" % renewUrl)

        renewReferer = "http://www.szlib.org.cn/MyLibrary/Loan-Status.jsp"
        headersForReqHtml["Referer"] = renewReferer

        data = self.getNetwordData(renewUrl, 8, dict(), headersForReqHtml)
        print "renew book, resp data", data
        if data:
            returnDate = parseReturnDate(data)
            if returnDate and len(returnDate) > 0 :
                respStr = '{"returndate":"%s"}' % returnDate
                self.sendSuccess(handler, respStr)
                self.mlog("renew succeed, return: %s" % respStr)
                return
        self.sendFailed(handler, 404, "renew %s failed!" % barcode)
        self.mlog("renew failed!")

    def toGetLoanHistory(self, handler, cardno, startDate, endDate):
        if self.cookie is None:
            self.sendFailed(handler, 404, "cookie is None!")
            return
        loanHistoryUrl = generalGetLoanHistoryUrl % (startDate, endDate, cardno, 1)
        self.mlog("loanHistoryUrl: %s" % loanHistoryUrl)
        data = self.getNetwordData(loanHistoryUrl, 8, None, headersForReqHtml)
        if data == False:
            self.sendFailed(handler, "404", "fetch loan history failed!")
        else:
            loanlist, totalno = getHistoryJsonFromXml(data.strip())
            self.mlog("get totalno: %d" % (totalno))
            pages = int(math.ceil(float(totalno) / 20.0))
            self.mlog("get %d pages" % pages);
            if pages >= 2:
                for page in range(2, pages+1):
                    loanHistoryUrl = generalGetLoanHistoryUrl %\
                            (startDate, endDate, cardno, page)
                    self.mlog("loanHistoryUrl: %s" % loanHistoryUrl)
                    data = self.getNetwordData(loanHistoryUrl, 8, None, headersForReqHtml)
                    if data == False:
                        self.mlog("fail in get %d page" % page)
                        break;
                    else:
                        loanlist_p, totalno = getHistoryJsonFromXml(data.strip())
                        loanlist.extend(loanlist_p)
            historyJson = json.dumps(loanlist)
            self.sendSuccess(handler, historyJson)
            #self.mlog("loan history: %s" % (historyJson))

    def login(self):
        postData = {"username":self.account, "password": self.pwdMd5}
        if self.post_base(szLibLogin, postData, headers=headersForReqHtml):
            self.hasLogin = True
        else:
            self.mlog("login failed")

    def post_base(self, url,  postData, headers):
        try:
            req = requests.post(szLibLogin, data=postData, headers=headers, timeout=G_REQUEST_TIMEOUT)
            if (req.status_code == 200):
                self.cookie = req.cookie
                return True
        except ConnectionError, e:
            self.mlog("failed to connet to server")
        except Timeout, e:
            self.mlog("time out")
        except HTTPError, e:
            self.mlog("response status is not 200: %s" % self.status_code)
        except request.exception.RequestException, e:
            self.mlog("unknow error:" + str(e))
        return False

    def fetchLoanList(self, handler):
        recordno = getValFromCookie(self.cookie, "recordno")
        loadUrl = URL_NEW_LOANLIST % (recordno)
        req = requests.get(loadUrl, timeout=G_REQUEST_TIMEOUT)
        infoList = json.loads(req.text)
        #self.mlog(infoList)
        loanlist = [item["meta"] for item in infoList if item.get("meta") is not None]
        loanJson = json.dumps(loanlist)
        self.sendSuccess(handler, loanJson)
        self.mlog(loanJson)

    def renewBook(self, loanInfo):

        pass

if __name__ == "__main__":


    account = "0440050867306"
    password = "19911213"
    pwd_md5 = md5.new(password).hexdigest()
    print "pwd_md5: %s" % (pwd_md5)
    postData = {"username":account, "password": pwd_md5}

    #cookie = setUpCookie()
    #rawHtml = getNetwordData(szLibLogin, 10, postData, headersForReqHtml)
    #print "request sent!"
    #print "%s" % rawHtml

    #bookList = getNetwordData(getLoanListUrl, 10, None, headersForReqHtml)
    #print bookList
    #print cookie

    if checkLegalISBN('978-7-121-24674-6'):
        print "true"
    else:
        print "false"

    if checkLegalISBN('978-7哈哈-5130-3913-0'):
        print "978-7哈哈-5130-3913-0 true"
    else:
        print "978-7哈哈-5130-3913-0 false"


