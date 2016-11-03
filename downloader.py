#coding:utf-8
'''
Created on 2016年11月2日
@author: 肖雄
'''
import requests
from multiprocessing.dummy import Pool, Lock
from progressbar import *

class DownLoader(object):
    '''
    分段下载
    每一个任务下载一个区块，并写入文件
    '''
    
    def __init__(self, url, file_path, block_size=1024):
        self.url = url
        self.file_path = file_path
        self.block_size = block_size
        self.lock = Lock()
        self.done = 0
        self.length = self.get_length()
        self.block_num = self.get_blocknum() 
        self.pool = self.get_pool()
        self.progress_show()
        
        
    def get_pool(self, process=None):
        
        if process and isinstance(process, int):
            return Pool(process)
        else:
            return Pool()
     
        
    def get_length(self):
        '''
        计算下载的总长度
        '''    
        
        res = requests.head(self.url)
        if res.ok:
            self.length = int(res.headers.get('content-length', 0))
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
        
        
        
    def open_file(self):
        self.f = open(self.file_path, 'wb')
     
        
    def close_file(self):
        self.f.close()
        
      
    def progress_show(self):
        '''
        进度条显示
        '''
        widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('>-=')),    \
           ' ', ETA(), ' ', FileTransferSpeed()]      
        self.pbar = ProgressBar(widgets=widgets, maxval=self.length).start()
         
         
                    
    def download_block(self, range):
        '''
        单线程下载指定区块
        '''    
        headers = {'Range': 'Bytes=%d-%d' % range}
        res = requests.get(self.url, headers=headers)
        if res.ok:
            self.lock.acquire()            
            self.f.seek(range[0])
            self.f.write(res.content)
            self.f.flush()
            
            if self.done == self.block_num - 1:
                self.pbar.update(self.length-1)               
            else:
                self.pbar.update(self.block_size * self.done) 
                
            self.done = self.done + 1  
            self.lock.release()
        else:
            pass
        
        
    def download(self):
         
        ranges = self.get_ranges()
        self.open_file()
        self.pool.map(self.download_block, ranges)
        self.pool.close() 
        self.pool.join()
        self.pbar.finish()
        self.close_file()
        
        
        
    