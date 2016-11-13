#coding:utf-8
'''
Created on 2016年11月5日
@author: superxiaoxiong
'''
import os

LOGGING_LEVEL = 'DEBUG'
LOGGING_FILE = os.path.expanduser(r'./.config/yundownload/yundownload.log')

DEFAULT_HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    }

BLOCK_SIZE = 1024*1024

RETRIES = 3
TIMEOUT = 50