#!/usr/bin/env python

import urllib, urllib2
import os
import math
from time import sleep
# Camera = AxisCamera('129.241.154.82', '/axis-cgi/com/', 'root', 'JegLikerKanelSnurrer')
clear = lambda: os.system('cls')

class AxisCamera(object):
    def __init__(self, ip, cgi_dir, usr, pwd):
        self.ip = ip
        self.cgi_dir = cgi_dir
        self.url = 'http://' + ip + cgi_dir
        self.ptz_url = self.url + 'ptz.cgi'
        self.usr = usr
        self.pwd = pwd
        self.stat_location = { 'pan':'0', 'tilt':'0', 'zoom':'0', 'focus':'0', 'brightness':'0', 'autofocus':'on', 'autoiris':'on' }
        self.password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        self.top_level_url = 'http://129.241.154.82/axis-cgi/com/'
        self.password_mgr.add_password(None, self.top_level_url, 'root', 'JegLikerKanelSnurrer')
        self.handler = urllib2.HTTPBasicAuthHandler(self.password_mgr)
        self.opener = urllib2.build_opener(self.handler)

    def execute_command(self, url, values):
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        try:
            response = self.opener.open(req)
            code = response.getcode()
        except urllib2.HTTPError as e:
            print e.code
            code = e.code
            print e.read()
        return code, response.read()


    def relative_pan(self, offset):
        values = { 'rpan' : str(offset)}
        code, html = self.execute_command(self.ptz_url, values)
        if code == 204:
            return True
        else:
            print 'pan failed'
            return False

    def tilt(self, offset):
        values = { 'rtilt' : str(offset)}
        code, html = self.execute_command(self.ptz_url, values)
        if code == 204:
            return True
        else:
            print 'pan failed'
            return False

    def go_home(self):
        values = { 'move' : 'home'}
        code, html = self.execute_command(self.ptz_url, values)
        if code == 204:
            return True
        else:
            print 'move home failed'
            return False
            
    def get_info(self):
        values = { 'info' : '1'}
        code, html = self.execute_command(self.ptz_url, values)
        print html
        if code == 200:
            return True
        else:
            print 'info failed'
            return False
            
    def update_location(self):
        values = { 'query' : 'position'}
        code, html = self.execute_command(self.ptz_url, values)
        location = html.strip('\r\n').split('\r\n')
        for item in location:
            left, right = item.split('=')
            self.stat_location.update({ str(left):str(right)})
        if code == 200:
            return True
        else:
            print 'info failed'
            return False
            
    def print_location(self):
        print "===== PrintLocation"
        for key, val in self.stat_location.iteritems():
            print key, "=>",val 
        return True