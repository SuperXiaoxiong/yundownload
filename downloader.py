#coding:utf-8
'''
Created on 2016年11月2日
@author: 肖雄
'''
import requests
from multiprocessing.dummy import Pool, Lock
from progressbar import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from copy import deepcopy
from config import DEFAULT_HEADERS, BLOCK_SIZE
from log import logger
from net import simple_request
from email import Message
import json
from log import logger


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_tmp_filepath(dir_name, file_name):
    '''返回最终路径名及临时路径名'''
    filepath = os.path.join(dir_name, file_name)
    return filepath, filepath + '.part', filepath + '.yundownload-stat'


class DownLoader(object):
    '''
    分段下载
    每一个任务下载一个区块，并写入文件
    '''
    
    def __init__(self, req, url, dirname, filename, block_size=BLOCK_SIZE):
        
        self.req = req
        self.url = url
        self.dir_name = dirname
        self.file_name = filename
        self.block_size = block_size
        self.lock = Lock()
        self.block_done = 0
        self.length = self.get_length()
        self.block_num = self.get_blocknum() 
        self.pool = self.get_pool()
        self.progress_show()
        self.status = 'LOAD'
        self.ranges_undo = []
        self.ranges_done = []
        
        
    def get_pool(self, process=None):
        
        if process and isinstance(process, int):
            return Pool(process)
        else:
            return Pool()
     
        
    def get_length(self):
        '''
        计算下载的总长度
        '''    
        
        res = self.req.head(self.url, headers=DEFAULT_HEADERS, verify=False)
        if res.ok:
            self.length = int(res.headers.get('content-length', 0))
            logger.debug(res.headers)
            logger.info(self.length)
            return self.length
        else:
            self.length = 0
            return self.length
        
        
    def get_blocknum(self):
        '''
        计算分块数量
        '''
        self.block_num = int(self.length + self.block_size -1) / self.block_size #向上取整      
        return self.block_num
        
        
    def get_ranges(self):
        '''
        计算分块下载时，各分块的下载范围
        '''
        ranges = []
        for i in range(self.block_num):
            if i == self.block_num - 1:
                ranges.append(( i * self.block_size, self.length))
            else:
                ranges.append(( i * self.block_size, (i + 1) * self.block_size))
        return ranges
        
               
      
    def progress_show(self):
        '''
        进度条显示
        '''
        widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('>-=')),    \
           ' ', ETA(), ' ', FileTransferSpeed()]      
        self.pbar = ProgressBar(widgets=widgets, maxval=self.length).start()
         
         
                    
    def download_block(self, range_):
        '''
        单线程下载指定区块
        ''' 
        
        if self.status == 'LOAD':  
            headers = deepcopy(DEFAULT_HEADERS)
            headers['Range'] = 'bytes=%d-%d' % range_
            for i in range(3):
                try:
                    res = self.req.get(self.url, headers=headers, verify=False)
                except Exception, e:
                    logger.error(e,Message)
                    logger.error('bytes=%d-%d download error' % range_  )
                    
                if res.ok:
                    self.lock.acquire()            
                    self.f.seek(range_[0])
                    self.f.write(res.content)
                    self.f.flush()
                    
                    if self.finished():
                        self.pbar.update(self.length-1)               
                    else:
                        self.pbar.update(self.block_size * self.block_done) 
                    
                    self.block_done = self.block_done + 1  
                    self.ranges_done.append(range_)
                    self.ranges_undo.remove(range_)
                    self.lock.release()
                    break
                else:
                    logger.warn(res.status_code)
                    logger.warn(res.request.headers)
                    logger.warn(res.headers)
                    
        elif self.status == 'PAUSE':
            pass 
                
        
        
    def download(self, ranges):
        try:
            logger.debug('download start')        
            self.pool.map(self.download_block, ranges)
            logger.debug('download end') 
            self.pool.close() 
            self.pool.join()
        finally:
            conf_info ={
                'block_done':self.block_done,
                'ranges_undo':self.ranges_undo,
                'ranges_done':self.ranges_done,
                }
            
            self.conf_fh.seek(0)
            self.conf_fh.write(json.dumps(conf_info))
        
        
        
    
    def pause(self):
        self.status = 'PAUSE'
        conf_info ={
                'block_done':self.block_done,
                'ranges_undo':self.ranges_undo,
                'ranges_done':self.ranges_done,
                }
        self.conf_fh.seek(0)
        self.conf_fh.write(json.dumps(conf_info))
        self.conf_fh.close()
        self.f.close()
        logger.info('have been pause')
        
        
                    
    def finished(self):
        if self.block_done >= self.block_num - 1:
            return True
        else:
            return False

              
    def run(self):
        

        filepath, tmp_filepath, conf_filepath = get_tmp_filepath(self.dir_name, self.file_name)
        
        logger.info('run start')
        if os.path.exists(tmp_filepath) and os.path.exists(conf_filepath):
            self.conf_fh = open(conf_filepath, 'r+')
            conf_f = json.load(self.conf_fh)
                # 已经下载的range，block_done, 还未下载的range
            self.f = open(tmp_filepath, 'rb+')
            self.block_done = conf_f['block_done']   
            ranges_undo = conf_f['ranges_undo']
            for each in ranges_undo:
                self.ranges_undo.append(tuple(each))
            ranges_done = conf_f['ranges_done']
            for each in ranges_done:
                self.ranges_done.append(tuple(each))          
        else:
            self.conf_fh = open(conf_filepath, 'w')
            self.f = open(tmp_filepath, 'wb')
            self.ranges_undo = self.get_ranges()
            self.ranges_done = []
            self.block_done = 0   
        
        logger.info('file_length  ' + str(self.length))
        logger.debug('block_done' + str(self.block_done))
        logger.debug('ranges_done' + str(self.ranges_done))
        logger.debug('ranges_undo' + str(self.ranges_undo))  
            
        res = simple_request(self.url, self.req)
        if not res:
            logger.error('Failed to get url to download')
        else:
            try:            
                self.download(self.ranges_undo)
            except Exception, e:
                if self.status == 'PAUSE':
                    logger.info(u'download stop')
                else:
                    logger.error(e.message)
        
        if not self.conf_fh.closed:
            self.conf_fh.close()
        if not self.f.closed:
            self.f.close()
        
        if self.finished():
            self.pbar.finish()
            os.rename(tmp_filepath, filepath)
            if os.path.exists(conf_filepath):
                os.remove(conf_filepath)
        else:
            pass
