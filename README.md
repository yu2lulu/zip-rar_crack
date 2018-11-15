
## describe
     author: jeffery.yu
     blog: www.yu2lulu.xyz
     time: 2018-11-15
     describe: 多进程zip/rar加密文件暴力破解
     python_version:3.7
     main： fp.extractall(path='.',pwd=password.encode('utf-8'))  密码错误抛出异常


## usage
    
    Usage: crack.py [options]
      Options:
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  暴力破解的文件
      -d PASSWDFILE, --dict=PASSWDFILE
                            暴力破解的字典
      -p PNUM, --process=PNUM
                            设置破解进程数

