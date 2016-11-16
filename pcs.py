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
    
def get_catalogs(content):
    dir_ = []
    if content:
        catalogs = content['list']
        for catalog in catalogs:
            dir_.append(catalog['server_filename'])
        return dir_
    else:
        return None