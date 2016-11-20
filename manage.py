#coding:utf-8
'''
Created on 2016年11月3日
@author: 肖雄
'''
import downloader
from log import logger
from auth import LoginWanpan
import os
import tool
import requests
import pcs
import config
import sys
import re
import urllib
import getopt



def login(username, password=None):
    '''
    登录模块:
    1.先用username查询是否有保存的cookies和bdstoken
    2.如果有则用cookies和bdstoken登录
    3.以上步骤失败则采取用户名和密码登录
    返回值:
    errno, req, bdstoken,
    errno 为0,代表登录成功, 为1代表登录失败
    req 为会话请求
    bdstoken 登录凭证
    '''
    login_wanpan = LoginWanpan()
    
    path_cookies = './session_saved/' + username + '_cookies'
    path_token =  './session_saved/' + username + '_token'
    if os.path.exists(path_cookies) and os.path.exists(path_token):
        cookies = tool.load_cookies_from_lwp(path_cookies)
        token = tool.load_auth(path_token)
        
        if cookies and token:
            
            req = requests.Session()
            req.cookies = cookies
            bdstoken = login_wanpan.get_bdstoken(req)
            
            if bdstoken:
                logger.info(u'cookies 和 token有效')
                return 0, req, bdstoken
            else:
                logger.info(u'cookies 或者 token无效')
                if password:
                    return login_wanpan.run(username, password)
                else:
                    return 1, None, None
        else:
            logger.info(u'cookies 或者 token 文件缺失或损坏')
            if password:
                return login_wanpan.run(username, password)
            else:
                return 1, None, None
    else:
        logger.info(u'没有登录记录')
        if password:
            return login_wanpan.run(username, password)
        else:
            return 1, None, None
        
        

def phelp():
    print u"""
    Welcome to yundownload!
    quit----------------------退出程序
    cd [路径]------------------切换目录
    ls -----------------------展示当前目录文件
    pwd-----------------------打印当前目录
    down [文件名] [下载路径]-----------下载文件至本地
    ?-------------------------打印此帮助信息
    """


def usage_login():
    print 'Usage: manage.py -u username '
    print '-p --password=password'
    print '-h --help'
    sys.exit(0)
    
    

def download(req, now_path, *cmd):
    
    cmd = cmd[0]  #*  变成了一个元组
    if len(cmd) < 2 or len(cmd) > 3:
        print cmd
        print u'参数错误  down 文件名 保存目录(默认e:/tmppic) '
        return 
    
    if len(cmd) == 2:
        dirname = r'e:/tmppic'
    else:
        dirname = cmd[2]
        
    filename = cmd[1]
    
    filename = now_path + filename
    filename = filename.encode('utf-8')
    url = 'http://pcs.baidu.com/rest/2.0/pcs/file?path=' + urllib.quote(filename) + '&method=download&app_id=266719'
    download = downloader.DownLoader(req, url, dirname, filename)
    download.run()
    return



def main():
    
    if not len(sys.argv[1:]):
        usage_login()
        
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hu:p:', ['help', 'username', 'password'])
    except getopt.GetoptError, reason:
        logger.error(reason.message)
        usage_login()
    
    username = None
    password = None
    
    for o,a in opts:
        if o in ('-h', '--help'):
            usage_login()
        elif o in ('-u', '--username'):
            username = a
        elif o in ('-p', '--password'):
            password = a
        else:
            assert False, 'Unhandled Option'
                
                
    if username:       
        if password:
            error, req, bdstoken = login(username, password)
        else:
            error, req, bdstoken = login(username)
    else:
        print 'no username'
    
    now_path = u'/'
    error, content = pcs.list_dir(req, bdstoken=bdstoken, headers=config.DEFAULT_HEADERS, path=now_path)  #初始环境置为根目录
    
    while True:
        catalogs = pcs.get_catalogs(content)
        cmd = raw_input('[#'+now_path.encode(sys.stdout.encoding)+']>>')        # 终端提示符
        cmd = cmd.strip()            # 去掉两端空格
        cmd = cmd.decode(sys.stdin.encoding)
        if '' == cmd:
            continue
        if 'quit' == cmd:            # 键入"quit"退出程序
            print 'quit'
            break
        cmd = re.split(r'\s+', cmd)  # 分离命令生成列表
        
        print cmd
        
        if 'cd' == cmd[0]:
            temp = now_path
            temp_content = content
            if cmd[1] == r'..':      # 返回上一级目录
                try:
                    now_path = now_path[:-1]
                    now_path = now_path[:now_path.rfind(r'/')+1]
                    error, content = pcs.list_dir(req, bdstoken=bdstoken, headers=config.DEFAULT_HEADERS, path=now_path)  
                    if error is not 0:
                        now_path = temp
                        content = temp_content
                        print 'No such file or directory'
                except:
                    now_path = temp
                    content = temp_content
                    print 'No such file or directory'
            else:
                print catalogs
                if cmd[1] in catalogs:                    # 进入特定目录
  
                    try:
                        now_path = now_path + cmd[1] + '/' #注意这里，加了/ 
                        print now_path

                        error, content = pcs.list_dir(req, bdstoken=bdstoken, headers=config.DEFAULT_HEADERS, path=now_path)
                        print error
                        if error is not 0:
                            now_path = temp
                            content = temp_content
                            print '222 No such file or directory'
                    except Exception, e:
                        logger.error(e.message)
                        now_path = temp
                        content = temp_content
                        print '333 No such file or directory'
                else:

                    print '444 No such file or directory'
        
        elif 'ls' == cmd[0]:
            if catalogs:
                for catalog in catalogs:
                    print catalog
        elif 'pwd' == cmd[0]:
            print now_path
        elif 'down' == cmd[0]:
            download(req, now_path, cmd)            
        elif '?' == cmd[0]:
            phelp()
        else:
            print 'command not found'
            phelp()
    
    
if __name__ == '__main__':
    main()