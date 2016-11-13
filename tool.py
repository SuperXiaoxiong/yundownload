#coding:utf-8
'''
Created on 2016年11月12日
@author: superxiaoxiong
'''

import base64
from log import logger
import json

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

    

def RSA_encrypt(message):
    '''用RSA加密字符串.
    public_key - 公钥
    message    - 要加密的信息, 使用UTF-8编码的字符串
    @return    - 使用base64编码的字符串
    '''
    # 如果没能成功导入RSA模块, 就直接返回空白字符串.
    
    with open('master-public.key','r') as f:
        public_key = f.read()
    
    print public_key    
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_v1_5.new(rsakey)
    encrypted = rsakey.encrypt(message.encode())
    return base64.encodestring(encrypted).decode().replace('\n', '')

def json_loads_single(s):
    '''处理不标准JSON结构化数据'''
    return json.loads(s.replace("'", '"').replace('\t', ''))