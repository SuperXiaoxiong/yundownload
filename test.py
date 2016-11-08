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

def test_log():
    logger.info('test')
    
    
def test_download():
    url = ''
    dirname = r'E:/tmppic/'
    filename = r'yang.jpg'
    req = requests.Session()
    downloader = DownLoader(req, url, dirname, filename)
    t = threading.Thread(target=downloader.run,args=())
    t.setDaemon(True)
    t.start()
    while True:
        if not t.is_alive():
            logger.info('download finished!' + filename)
            sys.exit()
        
        try:
            cmd = raw_input('请输入')
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
        
#test_download()
test_download()

    