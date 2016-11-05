#coding:utf-8
'''
Created on 2016年11月5日
@author: superxiaoxiong
'''
import os

LOGGING_LEVEL = 'INFO'
LOGGING_FILE = os.path.expanduser(r'./.config/yundownload/yundownload.log')

DEFAULT_HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    }

RETRIES = 3
TIMEOUT = 50