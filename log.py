#coding:utf-8
'''
Created on 2016年11月5日
@author: superxiaoxiong
'''

import logging
from logging.handlers import RotatingFileHandler
from config import LOGGING_FILE, LOGGING_LEVEL
import sys
import os


def _init_loger(log_level, max_bytes=1024*1024, backup_count=5):
    log_file = LOGGING_FILE
    dir_name = os.path.dirname(log_file)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except Exception, e:
            print e.message
            sys.exit(1)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')
    fd = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    fd.setLevel(log_level)
    fd.setFormatter(formatter)
    logger = logging.getLogger('yundownload')
    logger.setLevel(log_level)
    logger.addHandler(fd)
    return logger

logger = _init_loger(LOGGING_LEVEL)
