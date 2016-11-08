#coding:utf-8
'''
Created on 2016年11月7日
@author: superxiaoxiong
'''
import requests
from log import logger
import traceback

def simple_request(url, req, retries=3, timeout=50):
    for i in range(retries):
        try:
            res = req.get(url, stream=True, timeout=timeout, verify=False)
            #res = req.get(url, timeout=timeout, verify=False)
            return res
        except Exception, e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
    
    return None