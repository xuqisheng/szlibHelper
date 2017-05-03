#!/usr/bin/env python
#-*-coding=utf-8-*-

import socket, os
import BaseHTTPServer, SimpleHTTPServer
import ssl
import testFetchSzlib
from testFetchSzlib import log, UserInfoDef

CERT_PATH = "/home/april/cert/214067218810640.pem"
KEY_PATH = "/home/april/cert/214067218810640.key"

gUserDict = dict()

class MiniProgramHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):  
    def setup(self):  
        self.connection = self.request  
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)  
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)  
  
    def do_GET(self):  
        try:  
            self.send_response(200) 
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("DO NOT SUPPORT GET")
        except IOError:
            self.send_error(404, 'DO NOT SUPPORT GET')

    def do_POST(self):  
        try:  
            print 'path:', self.path

            # get post data
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length)
            print post_data

            # parse post data
            items = post_data.split('&')
            attrDict = dict()
            for item in items:
                vals = item.split('=')
                attrDict[vals[0]] = vals[1]

            account = attrDict.get("username")
            passwdMd5 = attrDict.get("password")
            postData = attrDict
            print postData

            if account is None or passwdMd5 is None:
                self.send_error(401, 'username or password is empty!')
                return

            # find the user from dictionay
            userInfo = gUserDict.get(account)
            if userInfo is None:
                userInfo = UserInfoDef(account, passwdMd5)
            userInfo.handleRequest(postData, self)

            ## setup cookie
            #cookie = testFetchSzlib.setUpCookie()

            ## fetch data from szlib
            #rawHtml = getNetwordData(testFetchSzlib.szLibLogin,
            #        10, postData, testFetchSzlib.headersForReqHtml)

            ## fetch loan list
            #bookList = getNetwordData(testFetchSzlib.getLoanListUrl,
            #        10, None, testFetchSzlib.headersForReqHtml)

            #self.send_response(200) 
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()
            #self.wfile.write(bookList)

        except IOError:
            self.send_error(404, 'IOError in server!')

if __name__ == "__main__":

    httpd = BaseHTTPServer.HTTPServer(('www.jiangfuqiang.cn', 443), MiniProgramHandler)

    httpd.socket = ssl.wrap_socket (httpd.socket,
            keyfile=KEY_PATH,
            certfile=CERT_PATH, server_side=True)

    httpd.serve_forever()
    pass

