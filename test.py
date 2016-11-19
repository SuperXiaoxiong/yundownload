#coding:utf-8
'''
Created on 2016年11月5日
@author: superxiaoxiong
'''
from log import logger
from downloader import DownLoader
import requests
import net
import sys
import threading
from auth import LoginWanpan
import pcs
import tool
import os
import config
import urllib

def test_log():
    logger.info('test')
    
    
def test_download():
    req, bdstoken = test_login()
    #url = url
    dirname=r'e:/tmppic'
    filename='scorpion.mp4'
    #req = requests.Session()
    
    url = 'http://pcs.baidu.com/rest/2.0/pcs/file?path=' + urllib.quote('/Scorpion.S03E08.720p.HDTV.NCARBBS.X264-DIMENSION.chs.eng') + '&method=download&app_id=266719'
 
     


    downloader = DownLoader(req, url, dirname, filename)
    t = threading.Thread(target=downloader.run,args=())
    t.setDaemon(True)
    t.start()
    while True:
        if not t.is_alive():
            logger.info('download finished!' + filename)
            sys.exit()
        
        try:
            cmd = raw_input(u'请输入')
        except (KeyboardInterrupt, SystemExit):
            print u'quit '
            logger.info('test quit ') 
            downloader.pause()
            sys.exit(0)
        else:
            cmd = cmd.decode(sys.getfilesystemencoding())
            if cmd == 'pause':
                print u'pause '
                logger.info('test pause')
                downloader.pause()
            elif cmd == 'load':
                print u'load '
                logger.info('test load ')
                downloader = DownLoader(req, url, dirname, filename)
                t = threading.Thread(target=downloader.run,args=())
                t.setDaemon(True)
                t.start()
        

def test_simple_requests():
    url = 'https://c.pcs.baidu.com/rest/2.0/pcs/file?metho'
    req = requests.Session()
    res = net.simple_request(url, req)
    if res.ok:
        print res.headers
        print res.request.headers
        print res.status_code
        print res.reason
    else:
        print 'no'
        
def test_login():
    login_wanpan = LoginWanpan()
    
    
    token = login_wanpan.load_auth()
    if os.path.exists('./cookies'):
        cookies = tool.load_cookies_from_lwp('./cookies')
        print cookies
        print token
        req = requests.Session()
        req.cookies = cookies
        bdstoken = login_wanpan.get_bdstoken(req)
        return req, bdstoken
        
    else:
        return login_wanpan.run()
       
    #req = login_wanpan.run()
    

def qr_check():
    import re
    res = {"errInfo":{        "no": "0"    },    "data": {        "codeString" : "jxG7f06c1fe8571e21f022314d54301417e776a9807b9017bc7",        "vcodetype" : "4ea5vlvQPdjy2odW8u8ETdqBkGiN3YfP777DbFPoig9e0h9NfRN7s4lOqMzP42a61LAD5WR4EEJNtFqfa9AFRkqiCCCDXOxX8491",        "userid" : "",        "mobile" : ""    }}
    
    res = str(res)
    logger.debug(res)
    print res
    #\s*"vcodetype"\s*:\s*"(\w*)"
    pm = re.search(r'\'codeString\'\s*:\s*\'(\w*)\',\s*\'vcodetype\'\s*:\s*\'(\w*)\'', res)
    if pm:
        codeString = pm.group(1)
        vcodetype = pm.group(2)
        print codeString,vcodetype
        
def key_check():
    import re
    res = r'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCtkCrB468BmyT\/dsXYYjC5hYqF\nKD3nO5SGUu33MH4Iw++uUyW5I8IppgXNWcXqvMrUyxuWg9Z\/ryRevCm4P4zMpyhs\nMpBOi81s6H8L8J6OeTyC3b4pkkHDVFPhZVBGLjMb3xB+KGB3o0rV5R1ohXDwooEN\nqHKmMROwGoaQBHk\/mQIDAQAB\n-----END PUBLIC KEY-----\n'
    public_key = re.search(r'-----BEGIN PUBLIC KEY-----\n(.*?)-----END PUBLIC KEY-----\n', res)
    print public_key.group(1)
    

def test_get_dlink(req, bdstoken, path):
    pcs.get_metas(req, bdstoken, path)
#test_log()
test_download()

#key_check()

#req, bdstoken = test_login()
'''
test_get_dlink(req, bdstoken, u'/系统')
test_get_dlink(req, bdstoken, '/forensic.7z')
   '''

