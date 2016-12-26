# yundownload
 百度云下载器

越来越依赖于百度网盘，于是想写一个同时支持win和linux的百度云shell程序

**如果觉得好，请给项目点颗星来支持吧～～** 

有什么好的建议，或者发现bug,请在issue中提出，欢迎contributors！

### 安装依赖

下载功能已经完成

sudo pip install requests==2.11.1
sudo pip install progressbar==2.3
sudo pip install pycrypto

遇到src/MD2.c:31:20: fatal error: Python.h: No such file or directory
sudo apt-get install Python-dev //安装python开发版包

### 进度说明

完成下载器 11-09

已经完成了登录模块 11-14

shell 控制模块基本完成 11-19

登录模块重新改写 11-20

修改部分BUG,下载功能已经完成 12-26

### 使用方法

python mannage.py -u username -p password

如果已经存在cookie或者token模块可忽略password参数

#### 下载器单独使用

修改test.py中参数url下载链接,dirname下载目录,filename保存文件名,

然后使用python test.py即可调用程序

在download模块中类class模块中，改变参数block_size=1024大小即可改变每个下载任务下载单位大小(受制于任务过多，线程切换，消耗资源)，建议1024*1024


#### manage模块使用

quit----------------------退出程序

cd [路径]------------------切换目录

ls -----------------------展示当前目录文件

pwd-----------------------打印当前目录

down [文件名] [下载路径]-----------下载文件至本地

?-------------------------打印此帮助信息

### 目前进度

完成下载器。11-09

1.支持断点续传下载，使用Http协议headers头中的Range参数。

2.支持下载暂停，通过将已经下载部分写入配置文件，启动时读取

3.支持下载进度显示，调用progressbar模块处理下载进度显示

完成登录验证码模块 11-14

1.第一次登录成功可以将cookie，token保存起来，再次登录不必进行验证

PCS下载，shell控制模块基本完成 11-19

使用python manage.py 运行程序

修改影响使用的部分BUG 12-26

token和cookie过期删除

中文下载路径支持

下载模块完成，支持linux图形化(只有终端二维码如何显示？)
