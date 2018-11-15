'''
author: jeffery.yu
blog: www.yu2lulu.xyz
time: 2018-11-15
describe: 多进程zip/rar加密文件暴力破解
python_version:3.7
main： fp.extractall(path='.',pwd=password.encode('utf-8'))
        密码错误抛出异常
'''

from multiprocessing import Process,Manager
import zipfile,rarfile,os,time,sys
from optparse import OptionParser


def isfile(filename):
    '''
    param filename:
    return:
    describe:检查待破解文件是否存在
    '''
    if os.path.isfile(filename)==False:
        print("%s 文件不存在,请检查!" %filename)
        return 3

def crack(filename,inputQ,outputQ):
    '''
    param filename  rar/zip文件
    param inputQ    密码队列
    param outputQ   结果队列，用于与主程序通信
    return
    '''

    if zipfile.is_zipfile(filename):
        fp=zipfile.ZipFile(filename)
    elif rarfile.RarFile(filename):
        fp=rarfile.RarFile(filename)

    while True:
        try:
            password=inputQ.get(timeout=1)
        except Exception as e:
            outputQ.put(1)
            time.sleep(1)
            exit(1)

        if str(fp).startswith("<rar"):
            try:
                fp.extractall(path='.',pwd=password) #rar暴力破解
                outputQ.put(password)
                time.sleep(1)
            except Exception as e:
                print('\r PASS:%s ' %password,end='')
                continue
        else:
            try:
                fp.extractall(path='.',pwd=password.encode()) #rar暴力破解
                outputQ.put(password)
                time.sleep(1)
            except Exception as e:
                print('\r PASS:%s ' %(password),end='')
                continue

def main(file,passwd,pnum):
    '''
    describe:
        1.主要是把密码读取入inpputq队列
        2.创建暴力破解进程
        3.主进程控制破解进度
    '''
    filename=file
    passwdfile=passwd

    result=isfile(filename)


    inputQ=Manager().Queue()
    outputQ=Manager().Queue()
    try:
        with open(passwdfile,encoding='utf-8') as f:
            for passwd in f:
                passwd=passwd.strip()
                inputQ.put(passwd)
    except:
        print("字典%s不存在,请检查!" %passwdfile)
        exit()

    print("字典载入完毕")

    processPool=[]
    for i in range(1,int(pnum)):
        p=Process(target=crack,args=(filename,inputQ,outputQ))
        processPool.append(p)
        p.start()

    flag=0
    #qsize=inputQ.qsize()
    print("\r正在破解.......")
    while True:
        if flag==int(pnum):
            print("\nSorry,no passwd found!")
            break
        data = outputQ.get()
        if data==1:
            flag+=1
            time.sleep(0.1)
            continue
        else:
            print("\nfound passwd:",data)
            break
    for p in processPool:
        p.terminate()

    #print("finished!")

if __name__=="__main__":
    #1.判断获取的参数是否为空
    if len(sys.argv)==1:
        print("Usage: python crack.py -h")
        exit()
    optParser = OptionParser()

    optParser.add_option('-f','--file',dest='file',help='暴力破解的文件')
    optParser.add_option('-d','--dict',dest='passwdfile',help='暴力破解的字典',default='passwd')
    optParser.add_option('-p','--process',dest="pnum",help='设置破解进程数',default=4)
    option, args = optParser.parse_args()

    if option.file ==None:
        print("Usage: python crack.py -h")
        exit()
    main(option.file,option.passwdfile,option.pnum)
