from requests import get
from pyquery import PyQuery
from os import system
import ctypes
from sys import exit, argv

def install(link, name):
    print(f'开始安装 {name} ......')
    system(f"start cmd /K pip install {link}")  # /K 执行完不关闭

def fetch():
    while True:
        name = input('请输入需要安装的库名：')
        print(f'请稍候，正在搜索库 {name}，可能需要一段时间......')
        res = get('http://mirrors.aliyun.com/pypi/simple/')
        doc = PyQuery(res.text)
        if name.lower() in doc('a').text():
            print(f'已经搜索到库 {name} ！')
            res = get(f'http://mirrors.aliyun.com/pypi/simple/{name}/')
            a = PyQuery(res.text)('a')
            # 文件名提取
            file_list = a.text().split(' ')
            # 链接提取
            href_list = [i.attr('href').replace('../../', 'http://mirrors.aliyun.com/pypi/')
                         for i in a.items()]            # items 作为迭代器才可以获取所有属性！
            print('含有如下结果，请选择您需要安装的项：')
            for i, filename in enumerate(file_list):
                print(f'\t{i+1}. {filename}')
            n = input('请输入要安装的项的序号：')
            while not 0<= int(n)-1 < len(href_list):
                n = input('请输入要安装的项的序号：')
            # 开始安装
            install(href_list[int(n)-1], name)
            print()
        else:
            print(f'没找到库 {name}，请检查名称是否输入正确！')
            print()

# 判断是否有管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    # 只能在管理员权限运行
    if is_admin():
        fetch()
    else:
        # 重新执行获取管理员权限后的程序
        ctypes.windll.shell32.ShellExecuteW(None, "runas", argv[0], None, None, 1)
        exit(0)