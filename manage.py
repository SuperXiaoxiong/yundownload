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
import cmd


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


def phelp():
    print """
    Welcome to yundownload!  This is the help utility.
    quit----------------------退出程序
    cd [路径]------------------切换目录
    ls -----------------------展示当前目录文件
    pwd-----------------------打印当前目录
    dl [文件名]---------------下载文件至本地
    dld [文件夹名]------------递归下载文件至本地
    ?-------------------------打印此帮助信息
    """


if __name__ == '__main__':
    now_path = u'/'
    req, bdstoken = test_login()
    error, content = pcs.list_dir(req, bdstoken=bdstoken, headers=config.DEFAULT_HEADERS, path=now_path)  #初始环境置为根目录
    print error, content
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
                        print error, content  
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
        elif 'download' == cmd[0]:
            pass
        elif 'dld' == cmd[0]:
            pass
        elif '?' == cmd[0]:
            phelp()
        else:
            print 'command not found'
