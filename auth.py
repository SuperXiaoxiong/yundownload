#coding:utf-8
'''
Created on 2016年11月5日
@author: superxiaoxiong
'''
import requests
import copy
import config
from log import logger
import time
import re
import os
import sys
import webbrowser
import subprocess
import tool
import random
import pcs




def get_ppui_logintime():
    '''ppui_ligintime 这个字段, 是一个随机数.'''
    return str(random.randint(52000, 58535))



class LoginWanpan():
    
    def __init__(self):
        self.req = requests.Session()
        self.headers = copy.deepcopy(config.DEFAULT_HEADERS)
    
    
    def get_uid(self):
        '''
        "token" : "the fisrt two args should be string type:0,1!",
        '''
        url = 'https://yun.baidu.com'
        res = self.req.get(url=url, headers=self.headers, allow_redirects=False)
        
        
    def get_token(self):
        '''
        https://passport.baidu.com/v2/api/?getapi&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=1478745870202&class=login&gid=9CB34E3-C5C3-4209-B9A0-764F3974F8F9&logintype=basicLogin&callback=bd__cbs__kh1hxq
        获取token "token" : "ba5a1bbd70e237575c17443f6433fa52",
        '''
        url = ''.join(['https://passport.baidu.com/v2/api/?',
                       'getapi&tpl=netdisk&subpro=netdisk_web&apiver=v3',
                       '&tt=', str(int(time.time())*1000),  
                       '&class=login&logintype=basicLogin',    
                       ])
        res = self.req.get(url=url, headers=self.headers, allow_redirects=False)
        pm = re.search(r'\"token\"\s*:\s*\"(\w+)\"', res.content)
        token = pm.group(1)
        return token
    
    
    def check_login(self, token, username):
        '''
        进行登录验证, 主要是在服务器上验证这个帐户的状态.
    如果帐户不存在, 或者帐户异常, 就不需要再进行最后一步的登录操作了.
    这一步有可能需要输入验证码.
    返回的信息如下:
    bd__cbs__fbpmrk({"errInfo":{        "no": "0"    },    "data": {        "codeString" : "需要获取",        "vcodetype" : "需要获取",        "userid" : "",        "mobile" : ""    }})
    '&sub_source':'leadsetpwd',
        '''
        
        url = ''.join([
        'https://passport.baidu.com/v2/api/',
        '?logincheck',
        '&token=', token,
        '&tpl=netdisk&apiver=v3',
        '&tt=', str(int(time.time())*1000),
        '&subpro','netdisk_web',   
        '&username=', username,
        '&isphone=false',
    ])
        res = self.req.get(url=url, headers=self.headers, allow_redirects=False)
        
        #pm = re.search(r'"codeString"\s*:\s*"(\w*)",\s*"vcodetype"\s*:\s*"(\w*)"', res.content)
        #,\s*\"vcodetype\"\s*:\s*\"(\w*)\"
        codeString = re.search(r'\"codeString\"\s*:\s*\"(\w*)\"', res.content)
        vcodetype  = re.search(r'\"vcodetype\"\s*:\s*\"(.*?)\"', res.content)
        if codeString and vcodetype:
            return codeString.group(1), vcodetype.group(1)
        else:
            return None, None
        
    def get_signin_vcode(self, codeString):
        '''
     https://passport.baidu.com/cgi-bin/genimage?jxG1a07c1e0854cc1ce0234142443016b7f5fb74307fe017e85
        '''
        url = ''.join([
            'https://passport.baidu.com/cgi-bin/genimage?',
            codeString
                       ])
        res = self.req.get(url=url, headers=self.headers)
        data = res.content
        with open('./qrimg.png', 'wb') as img:
            img.write(data)
        qr_path = os.path.join('file:///',os.getcwd(),'qrimg.png')
        if sys.platform.startswith('win'):
            webbrowser.open(qr_path)
        elif sys.platform.find('linux')>= 0 :
            subprocess.call(['xdg-open', qr_path])    
        
        
    
    def refresh_signin_vcode(self, token, vcodetype):
        '''
        刷新验证码
        https://passport.baidu.com/v2/?reggetcodestr&token=d5560032869d2200e5305558cd4d7400&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=1478835661744&fr=login&vcodetype=6609hLJjp3C5wLNq%2FuRhWFVRHosn%2FB15Al%2B7J%2FCjpgfBXcbiwpNkqKvlHqsI8WcECGM3THJ55b0If8ZbbzsqBTGZ1c3y91ko4bFu&callback=bd__cbs__2o55sr
        bd__cbs__2o55sr({"errInfo":{        "no": "0"    },    "data": {        "verifyStr" : "jxG5c07c1e18544c12b02b614f04301347f93d943070d017e0e",        "verifySign" : ""    }})
        会响应一串verifyStr,获取verifyStr,再有get_signin_vcode获取验证码
        '''
        url = ''.join([
            'https://passport.baidu.com/v2/?',
            'reggetcodestr&token=',token,
            '&tpl=netdisk&subpro=netdisk_web&apiver=v3',
            '&tt=',str(int(time.time())*1000),
            '&fr=login&vcodetype=', vcodetype])
        res = self.req.get(url=url, headers=self.headers)
        verifyStr = re.search(r'\"verifyStr\"\s*:\s*\"(\w*)\"', res.content)
        return verifyStr.group(1)
    
    def get_public_key(self, token):
        import json
        '''
        请求url:https://passport.baidu.com/v2/getpublickey?token=d5560032869d2200e5305558cd4d7400&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=1478835650982&gid=1B7D4BB-5D98-46A7-B8F1-2F1D902E71D8&callback=bd__cbs__4aftty
        响应bd__cbs__4aftty({"errno":'0',"msg":'',"pubkey":'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCtkCrB468BmyT\/dsXYYjC5hYqF\nKD3nO5SGUu33MH4Iw++uUyW5I8IppgXNWcXqvMrUyxuWg9Z\/ryRevCm4P4zMpyhs\nMpBOi81s6H8L8J6OeTyC3b4pkkHDVFPhZVBGLjMb3xB+KGB3o0rV5R1ohXDwooEN\nqHKmMROwGoaQBHk\/mQIDAQAB\n-----END PUBLIC KEY-----\n',"key":'xhfrWztQBAc8uyJw8YgNYGuJp7m4Os62'})
        '''
        url = ''.join([
            'https://passport.baidu.com/v2/getpublickey?',
            'token=',token,
            '&tpl=netdisk&subpro=netdisk_web&apiver=v3',
            '&tt',str(int(time.time())*1000),])
        res = self.req.get(url=url, headers=self.headers)
        #print json.loads(res.content)
        public_key = re.search(r'KEY-----(.*?)-----END', res.content)
        public_key = public_key.group(1)[1:]
        #public_key = public_key.group(1).split('\n')[1]
        public_key = ''.join(['-----BEGIN PUBLIC KEY-----\\',public_key,'-----END PUBLIC KEY-----\n'])
        private_key = re.search(r'\"key\"\s*:\s*\'(\w*)\'', res.content)
        private_key = private_key.group(1)
        
        res = tool.json_loads_single(res.content)
        
        
        with open('master-public.key', 'w') as f:
            f.write(res['pubkey'])
        return private_key
        
    
    def post_login(self, token, username, password, rsakey, verifycode='', codestring=''):
        
        '''
        登录验证.
        password   - 使用RSA加密后的base64字符串
        rsakey     - 与public_key相匹配的rsakey
        verifycode - 验证码, 默认为空
        return (status, info). 其中, status表示返回的状态:
        0 - 正常, 这里, info里面存放的是auth_cookie
        -1 - 未知异常
        4 - 密码错误
        257 - 需要输入验证码, 此时info里面存放着(vcodetype, codeString))
        '''
        if verifycode != '':
            verifycode = verifycode.encode('utf-8')
        
        url = 'https://passport.baidu.com/v2/api/?login'
        data = {
            'staticpage':'https://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html',
            'charset':'utf-8',
            'token':token,
            'tpl':'netdisk',
            'subpro':'netdisk_web',
            'apiver':'v3',
            'tt':str(int(time.time())*1000),
            'codestring':codestring,
            'safeflg':'0',
            'u':'https://pan.baidu.com/disk/home',
            'detect':'1',
            'quick_user':'0',
            'logintype':'basicLogin',
            'logLoginType':'pc_loginBasic',
            'loginmerge':'true',
            'username':username,
            'password':password,
            'verifycode':verifycode,
            'mem_pass':'on',
            'rsakey':rsakey,
            'crypttype':12,
            'ppui_logintime':get_ppui_logintime(),
                        }
        #res = self.req.post(url, data=data, headers=self.headers, proxies=tool.proxies, verify=False)
        res = self.req.post(url, data=data, headers=self.headers)
        
        status = re.search(r'err_no=(\d+)', res.content) 
        vcodetype = re.search(r'vcodetype=(.*?)&', res.content)
                        
        tool.save_cookies_lwp(res.cookies, './session_saved/' + username + '_cookies')
        
        return int(status.group(1)), vcodetype.group(1)
    
    
    
    def get_bdstoken(self, req):
        url = 'https://pan.baidu.com/disk/home'
        res = req.get(url, headers=self.headers)
        bdstoken = re.search(r'\"bdstoken\":"(\w+)\"', res.content) 
        
        logger.debug(res.url)
        logger.debug(res.cookies)
        logger.debug(res.request.headers)
        logger.debug(res.headers)
        
        
        
        if bdstoken:
            return bdstoken.group(1)
        else:
            return None
 

    def run(self, username, password):
        
        
        self.get_uid()
        token = self.get_token()
        codeString, vcodetype = self.check_login(token, username)
        
        rsakey = self.get_public_key(token)
        
        password_crypto = tool.RSA_encrypt( password)
        
        
        
        if codeString and vcodetype:
            self.get_signin_vcode(codeString)
            #verifyStr = self.refresh_signin_vcode(token, vcodetype)
            input_verify = raw_input(u'请输入验证码'.encode(sys.stdin.encoding))
            input_verify = input_verify.decode(sys.stdin.encoding)
            #input_verify = input_verify.decode(sys.getfilesystemencoding()).encode('utf-8')
            err_no, vcodetype = self.post_login(token, username, password_crypto, rsakey, input_verify, codeString)
        else:
            err_no , vcodetype = self.post_login(token, username, password_crypto, rsakey)
        
        while err_no == 257:
            #没有验证码
            codeString = self.refresh_signin_vcode(token, vcodetype)
            self.get_signin_vcode(codeString)
            input_verify = raw_input(u'请输入验证码'.encode(sys.stdin.encoding))
            input_verify = input_verify.decode(sys.stdin.encoding)
            #input_verify = input_verify.decode(sys.getfilesystemencoding()).encode('utf-8')
            err_no, vcodetype = self.post_login(token, username, password_crypto, rsakey, input_verify, codeString)
            
        if err_no == 6:
            #验证码错误
            
            '''
            从返回中获取vcodetype
            '''
            print u'验证码错误'
            
            codeString = self.refresh_signin_vcode(token, vcodetype)
            self.get_signin_vcode(codeString)
            input_verify = raw_input(u'请输入验证码'.encode(sys.stdin.encoding))
            input_verify = input_verify.decode(sys.stdin.encoding)
            err_no, vcodetype = self.post_login(token, username, password_crypto, rsakey, input_verify, codeString)
            
            
            
        
         
        if err_no == 0:
            '''
            通过token获取bdstoken
            '''
            bdstoken = self.get_bdstoken(self.req)
            tool.dump_auth(token, './session_saved/' + username + '_token' )
            
            pcs.list_dir(self.req, headers=self.headers, bdstoken=bdstoken, path=r'/')
            return 0, self.req, bdstoken