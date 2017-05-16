#!/usr/bin/env python
#-*-coding=utf-8-*-

import socket, os
import ssl
import BaseHTTPServer, SimpleHTTPServer
from SocketServer import ThreadingMixIn
import testFetchSzlib
from testFetchSzlib import log, UserInfoDef, getSzlibBookCover

CERT_PATH = "/home/april/cert/214067218810640.pem"
KEY_PATH = "/home/april/cert/214067218810640.key"

gUserDict = dict()

class MiniProgramHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):  
    def setup(self):  
        self.connection = self.request  
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)  
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)  
  
    def do_GET(self):  
        print self.path
        if self.path.startswith("/getSzlibCover/"):
            isbn = self.path.split("/")[2].split('.')[0]
            print "the isbn: %s" % (isbn)
            #req = request.get(getLoanListUrl, params=urlParam)
            #print req.text
            imgData = testFetchSzlib.getSzlibBookCover(isbn)
            print "imgData len: %d" % len(imgData)
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(imgData)
        else:
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
            print 'post_data:', post_data

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
                gUserDict[account] = userInfo
            userInfo.handleRequest(postData, self)

        except IOError:
            self.send_error(404, 'IOError in server!')

class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    ''' BaseHTTPServer with threading '''

if __name__ == "__main__":

    httpd = ThreadedHTTPServer(('www.jiangfuqiang.cn', 443), MiniProgramHandler)

    httpd.socket = ssl.wrap_socket (httpd.socket,
            keyfile=KEY_PATH,
            certfile=CERT_PATH, server_side=True)

    httpd.serve_forever()
    pass

