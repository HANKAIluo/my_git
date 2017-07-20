import re
import requests
import time, os
from bs4 import BeautifulSoup

headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/56.0.2924.87 Safari/537.36',
           'Connection':'close'}
my_local = 'E:/LOCAL/'


def get_url():
    try:
        te = requests.get('http://www.v4.cc/wiki/1805', headers=headers, timeout=10)
        data = BeautifulSoup(te.text, 'lxml').findAll('div', {'class':'wikicon'})
        link_list = [ 'http://www.v4.cc' + i for i in re.findall(r"/News-[0-9]+.html", str(data))]
        all_picture_link = []
        for y in link_list[::-1]:    #列表从最后一集开始，所以倒序
            r = requests.get(y, headers=headers, timeout=10)
            all_ = BeautifulSoup(r.text, 'lxml').find('div', {'class':'detailcontent1'}).findAll('img')[:-1]
            for i in all_:
                all_picture_link.append(str(i)[10:-3])
            r.close()
            time.sleep(3)
    except Exception as e:
        print(e)
    print('success')
    return all_picture_link

def downlocal_picture(url, pic_nam=0):
    #主要下载操作
    try:
        for t in url:
            pic_nam += 1
            te = requests.get(t, headers=headers, timeout=10)
            picture_name = my_local + '{n}.jpg'.format(n=pic_nam)
            with open(picture_name, 'wb') as code:
                code.write(te.content)
            time.sleep(3)
            print(str(pic_nam)+'success')
    except Exception as e:
        print(e)

def is_path_exit():
    """断点继续"""
    path_name = 'E:/LOCAL/1.jpg'
    name = 0
    while os.path.exists(path_name):
        if name == 0:
            name = name + 2
        else:
            name += 1
        path_name = 'E:/LOCAL/' + '{n}.jpg'.format(n=name)
    return name

if __name__ == '__main__':
    name = is_path_exit()
    print(name)
    link = get_url()
    downlocal_picture(link, pic_nam=name)