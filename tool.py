#coding:utf-8
'''
Created on 2016年11月12日
@author: superxiaoxiong
'''

import base64
from log import logger
import json
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import cookielib
import os
import time


DELTA = 1 * 24 * 60 * 60

proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}



def save_cookies_lwp(cookiejar, filename):
        lwp_cookiejar = cookielib.LWPCookieJar()
        for c in cookiejar:
            args = dict(vars(c).items())
            args['rest'] = args['_rest']
            del args['_rest']
            c = cookielib.Cookie(**args)
            lwp_cookiejar.set_cookie(c)
        lwp_cookiejar.save(filename, ignore_discard=True)

def load_cookies_from_lwp(filename):
    lwp_cookiejar = cookielib.LWPCookieJar()
    lwp_cookiejar.load(filename, ignore_discard=True)
    return lwp_cookiejar
    
    
def RSA_encrypt(message):
    '''用RSA加密字符串.
    public_key - 公钥
    message    - 要加密的信息, 使用UTF-8编码的字符串
    @return    - 使用base64编码的字符串
    '''
    # 如果没能成功导入RSA模块, 就直接返回空白字符串.
    
    with open('master-public.key','r') as f:
        public_key = f.read()
    
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_v1_5.new(rsakey)
    encrypted = rsakey.encrypt(message.encode())
    return base64.encodestring(encrypted).decode().replace('\n', '')

def json_loads_single(s):
    '''处理不标准JSON结构化数据'''
    return json.loads(s.replace("'", '"').replace('\t', ''))


def load_auth(auth_file):
        
    # 如果授权信息被缓存, 并且没过期, 就直接读取它.
    if os.path.exists(auth_file):
        if time.time() - os.stat(auth_file).st_mtime < DELTA:
            with open(auth_file) as fh:
                token = json.load(fh)
            return token
    return None


def dump_auth(token, auth_file):
    with open(auth_file, 'w') as fh:
        json.dump([token], fh)    
            

def latency():
    '''返回操作时消耗的时间.
    这个值是0.1-1之前的五位小数, 用于跟踪服务器的响应时间.
    我们需要随机生成它.
    '''
    return str(random.random())[:7]