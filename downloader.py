#coding:utf-8
'''
Created on 2016年11月2日
@author: 肖雄
'''
import requests
from multiprocessing.dummy import Pool, Lock


class DownLoader(object):
    '''
    分段下载
    每一个任务下载一个区块，并写入文件
    '''
    
    def __init__(self, url, file_path=None, block_size=1024):
        self.url = url
        self.file_path = file_path
        self.block_size = block_size
        self.lock = Lock()
        
    
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
            length = int(res.headers.get('content-length', 0))
            return length
        else:
            length = 0
            return length
        
        
    def get_blocknum(self, length):
        '''
        计算分块数量
        '''
        self.block_num = int(length + self.block_size -1) / self.block_size #向上取整      
        
        
    def get_ranges(self, length=0):
        '''
        计算分块下载时，各分块的下载范围
        '''
        if length is not 0:
            ranges = range(0, length, self.block_size)
            ranges = [(start, start + self.block_size) for start in ranges]
            return ranges
        else:
            return [(0,'')]
        
        
        
    def open_file(self):
        #self.f = os.open(self.file_path, os.O_RDONLY|os.O_CREAT)
        #self.f = os.fdopen(self.f, "w+")
        self.f = open(self.file_path, 'wb')
        
    def close_file(self):
        self.f.close()
        
                 
    def download_block(self, range):
        '''
        单线程下载指定区块
        '''    
        headers = {'Range': 'Bytes=%d-%d' % range}
        res = requests.get(self.url, headers=headers)
        if res.ok:
            self.lock.acquire()            
            self.f.seek(range[0])
            print  self.f.tell() , range[0]   
            self.f.write(res.content)
            self.lock.release()
        else:
            pass
        
        
    def download(self):
        pool = self.get_pool()
        length = self.get_length()
        ranges = self.get_ranges(length)
        self.open_file()
        pool.map(self.download_block, ranges)
        pool.close() 
        pool.join()
        self.close_file()
        
        
        
    