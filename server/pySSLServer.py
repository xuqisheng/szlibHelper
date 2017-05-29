#!/usr/bin/env python
#-*-coding=utf-8-*-

import time
from threading import Thread
import socket, os
import ssl
import BaseHTTPServer, SimpleHTTPServer
from SocketServer import ThreadingMixIn
import testFetchSzlib
from testFetchSzlib import log, UserInfoDef, getSzlibBookCover

CERT_PATH = "/home/april/cert/214067218810640.pem"
KEY_PATH = "/home/april/cert/214067218810640.key"

gUserDict = dict()
#gBandDict = dict()

def doClean(userDict):
    for (key, user) in userDict.items():
        user.lifecount -= 1;
    for (key, user) in userDict.items():
        if user.inUsing < 1 and user.lifecount <= 0:
            userDict.pop(key, None)
            print "pop user:", user.account

def cleanUserDict(userDict, interval):
    while(1):
        #print "going to do clean, has %d users" % len(userDict)
        doClean(userDict)
        time.sleep(interval);

class MiniProgramHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):  
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)
  
    def sendFailed(self, code, content):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        print "GET req, path:", self.path
        if self.path.startswith("/getSzlibCover/"):
            isbn = self.path.split("/")[2].split('.')[0].strip()
            if testFetchSzlib.checkLegalISBN(isbn):
                print "the isbn: %s" % (isbn)
                imgData = testFetchSzlib.getSzlibBookCover(isbn)
                print "imgData len: %d" % len(imgData)
                try:  
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(imgData)
                except IOError:
                    self.send_error(404, 'DO NOT SUPPORT GET')
                    print "IO Error when sending imgData!"
                return
            else:
                print "illegal isbn:", isbn
        else:
            print "GET path is wrong!"

        try:
            self.send_response(200) 
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("DO NOT SUPPORT GET")
            print "Send error to GET request done!"
        except IOError:
            self.send_error(404, 'DO NOT SUPPORT GET')
            print "IO Error when sending error to GET request!"

    def do_POST(self):
        try:
            print 'POST req, path:', self.path

            # get post data
            length = int(self.headers['Content-Length'])
            if (length is None or length == 0):
                print "req post data length is None or 0"
                return

            post_data = ""
            try:
                post_data = self.rfile.read(length)
                print 'raw post_data:', post_data
            except IOError:
                self.send_error(500, 'IO Error when reading post data!')
                print "IO Error when reading post data!"
                return

            # parse post data
            items = post_data.split('&')
            attrDict = dict()
            for item in items:
                vals = item.split('=')
                attrDict[vals[0]] = vals[1]

            account = attrDict.get("username")
            passwdMd5 = attrDict.get("password")
            postData = attrDict
            print "post data dict:", postData

            if account is None or passwdMd5 is None:
                self.send_error(401, 'username or password is empty!')
                return

            # find the user from dictionay
            userInfo = gUserDict.get(account)
            if userInfo is None:
                userInfo = UserInfoDef(account)
                gUserDict[account] = userInfo
            else:
                userInfo.lifecount = testFetchSzlib.G_USER_LIFE_COUNT

            userInfo.inUsing += 1
            try:
                userInfo.handleRequest(postData, self)
                userInfo.inUsing -= 1
            except IOError:
                self.send_error(500, 'IO Error when handling request!')
                userInfo.inUsing -= 1
                print "IO Error when handling request!"

        except IOError:
            self.send_error(404, 'IOError in server!')
            print "IO Error when handling request!"

class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    ''' BaseHTTPServer with threading '''

if __name__ == "__main__":

    httpd = ThreadedHTTPServer(('www.jiangfuqiang.cn', 443), MiniProgramHandler)

    httpd.socket = ssl.wrap_socket (httpd.socket,
            keyfile=KEY_PATH,
            certfile=CERT_PATH, server_side=True)

    # timer function to clean userInfoDict
    cleanThread = Thread(target=cleanUserDict, args = (gUserDict, 60))
    cleanThread.daemon = True
    cleanThread.start()
    print "Clean thread Started!"

    httpd.serve_forever()
    print "Server Ended!"

