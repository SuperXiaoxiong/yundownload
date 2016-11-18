#coding:utf-8
'''
Created on 2016年11月13日
@author: superxiaoxiong
'''

import time
import tool
import config
import urllib
from log import logger
import json
import sys
import downloader


def list_dir(req,  bdstoken, headers, path, page=1, num=100):
    '''得到一个目录中的所有文件的信息(最多100条记录).'''
    path = path.encode('utf-8')
    timestamp = str(int(time.time())*1000)
    url = ''.join([
        'http://pan.baidu.com/api/',
        'list?channel=chunlei&clienttype=0&web=1',
        '&num=', str(num),
        '&t=', timestamp,
        '&page=', str(page),
        '&dir=', urllib.quote(path,safe=''),
        '&t=', tool.latency(),
        '&order=time&desc=1',
        '&_=', timestamp,
        '&bdstoken=', str(bdstoken),
    ])
    #res = req.get(url,  headers=config.DEFAULT_HEADERS, proxies=tool.proxies, verify=False)
    res = req.get(url,  headers=headers)
    if res.content:
        content = json.loads(res.content)
        errno = content['errno']
        
        return errno, content
    
    return None, None


'''
def get_download_link(req, bdstoken, path):
    在下载之前, 要先获取最终的下载链接.
    path - 一个文件的绝对路径.
    @return red_url, red_url 是重定向后的URL, 如果获取失败,
            就返回原来的dlink;
    
    metas = get_metas(req, bdstoken, path)
    if (not metas or metas.get('errno', -1) != 0 or
            'info' not in metas or len(metas['info']) != 1):
        logger.error('pcs.get_download_link(): %s' % metas)
        return None
    dlink = metas['info'][0]['dlink']
    url = '{0}&cflg={1}'.format(dlink, cookie.get('cflag').value)
    req = net.urlopen_without_redirect(url, headers={
        'Cookie': cookie.sub_output('BAIDUID', 'BDUSS', 'cflag'),
        'Accept': const.ACCEPT_HTML,
    })
    if not req:
        return url
    else:
        return req.getheader('Location', url)
'''
     
    
def get_metas(req, bdstoken, filelist, headers=config.DEFAULT_HEADERS, dlink=True):
    '''获取多个文件的metadata.
    filelist - 一个list, 里面是每个文件的绝对路径.
               也可以是一个字符串, 只包含一个文件的绝对路径.
    dlink    - 是否包含下载链接, 默认为True, 包含.
    @return 包含了文件的下载链接dlink, 通过它可以得到最终的下载链接.
    '''
    
    
    filelist = filelist.encode('utf-8')
    print filelist
    
    

    
    if isinstance(filelist, str):
        filelist = [filelist, ]
    url = ''.join([
        'http://pan.baidu.com/api/',
        'filemetas?channel=chunlei&clienttype=0&web=1',
        '&bdstoken=', bdstoken,
    ])
    
    if dlink:
        data = {
            'dlink':1,
            'target':json.dumps(filelist)
            }
    else:
        data = {
            'dlink':0,
            'target':json.dumps(filelist)
            }
        print data
    res = req.post(url=url, data=data, headers=headers)
    if res:
        content = json.loads(res.content)
        print content
        if content['errno'] == 0:
            info = content['info']
            if info[0]['isdir'] == 1:
                print filelist, 'isdir'
            elif info[0]['isdir'] == 0:
                dlink = info[0]['dlink']
                print dlink
                print res.cookies
                print req.cookies
                print res.headers
                
        else:
            print 'get no link'
        
    else:
        print 'not get dlink'
        return None
    
    
    


 
def get_catalogs(content):
    dir_ = []
    if content:
        catalogs = content['list']
        for catalog in catalogs:
            dir_.append(catalog['server_filename'])
        return dir_
    else:
        return None
    
