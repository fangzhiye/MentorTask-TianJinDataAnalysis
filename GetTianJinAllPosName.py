#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author=He

"""
通过国家统计局数据
获取中国所有城市列表
"""
import sys
import os
import re
import codecs
from urllib import request
from bs4 import BeautifulSoup
TianJinAllLocation = []

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'
header = {
    'Cookie': 'AD_RS_COOKIE=20080917',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \ AppleWeb\Kit/537.36 (KHTML, like Gecko)\ '
                  'Chrome/58.0.3029.110 Safari/537.36'}


class GetHttp:
    def __init__(self, url, headers=None, charset='utf8'):
        if headers is None:
            headers = {}
        self._response = ''
        try:
            print(url)
            self._response = request.urlopen(request.Request(url=url, headers=headers))
        except Exception as e:
            print(e)
        self._c = charset

    @property
    def text(self):
        try:
            return self._response.read().decode(self._c)
        except Exception as e:
            print(e)
            return ''


def provincetr(u, he, lists):
    # 获取全国省份和直辖市
    t = GetHttp(u, he, 'gbk').text
    if t:
        soup = BeautifulSoup(t, 'html.parser')
        for i in soup.find_all(attrs={'class': 'provincetr'}):
            for a in i.find_all('a'):
                id = re.sub("\D", "", a.get('href'))
                if(a.text =='天津市'):
                    lists[id] = {'id': id, 'name': a.text, 'pid': '0', 'pid1': '0', 'pid2': '0', 'pid3': '0', 'pid4': '0',
                             'code': id}
                    TianJinAllLocation.append(a.text)
                    break
                else :
                    continue
                # time.sleep(1 / 10)
    return lists #list是一个数组，在这只有一个元素就是天津
#p = provincetr(u=url, he=header, lists={})


def citytr(u, he, lists):
    # 获取省下级市
    l = lists.copy()
    for i in l:
        t = GetHttp(u+i+'.html', he, 'gbk').text
        if not t:
            continue
        soup = BeautifulSoup(t, 'html.parser')
        for v in soup.find_all(attrs={'class': 'citytr'}):
            id = str(v.find_all('td')[0].text)
            if id[0:4] not in lists.keys():
                lists[id[0:4]] = {'id': id[0:4], 'name': str(v.find_all('td')[1].text),
                                  'pid': '0', 'pid1': i, 'pid2': '0', 'pid3': '0', 'pid4': '0', 'code': id}
                TianJinAllLocation.append(lists[id[0:4]]['name'])
    return lists


def countytr(u, he, lists):
    # 获取市下级县
    l = lists.copy()
   # a = {}
    for i in l:
        t = GetHttp(u+i[0:2]+'/'+i+'.html', he, 'gbk').text
        if not t:
            continue
        soup = BeautifulSoup(t, 'html.parser')
        for v in soup.find_all(attrs={'class': 'countytr'}):
            id = str(v.find_all('td')[0].text)
            if id[0:6] not in lists.keys():
                lists[id[0:6]] = {'id': id[0:6], 'name': str(v.find_all('td')[1].text),
                                  'pid': '0', 'pid1': l[i]['pid1'], 'pid2': i, 'pid3': '0', 'pid4': '0', 'code': id}
                TianJinAllLocation.append(lists[id[0:6]]['name'])
    return lists


def towntr(u, he, lists):
    # 县下级镇
    l = lists.copy()
    for i in l:
        t = GetHttp(u+i[0:2]+'/'+i[2:4]+'/'+i+'.html', he, 'gbk').text
        if not t:
            continue
        soup = BeautifulSoup(t, 'html.parser')
        for v in soup.find_all(attrs={'class': 'towntr'}):
            id = str(v.find_all('td')[0].text)
            if id[0:9] not in lists.keys():
                lists[id[0:9]] = {'id': id[0:9], 'name': str(v.find_all('td')[1].text), 'pid': '0',
                                  'pid1': l[i]['pid1'], 'pid2': l[i]['pid2'], 'pid3': i, 'pid4': '0', 'code': id}
                TianJinAllLocation.append(lists[id[0:9]]['name'])
    return lists


def villagetr(u, he, lists):
    # 镇下级村
    l = lists.copy()#拷贝lists数组
    for i in l:     #遍历list数组
        t = GetHttp(u+i[0:2]+'/'+i[2:4]+'/'+i[4:6]+'/'+i+'.html', he, 'gbk').text #获得Http请求的正文
        if not t:
            continue #如果http的正文不存在就忽略不管了
        soup = BeautifulSoup(t, 'html.parser')#解析正文吧
        for v in soup.find_all(attrs={'class': 'villagetr'}):
            id = str(v.find_all('td')[0].text)
            if id[0:12] not in lists.keys():    #0:12是村的编码吧
                lists[id[0:12]] = {'id': id[0:12], 'name': str(v.find_all('td')[2].text), 'pid': '0',
                                   'pid1': l[i]['pid1'], 'pid2': l[i]['pid2'], 'pid3': l[i]['pid2'], 'pid4': i,
                                   'code': id}
                villageName = lists[id[0:12]]['name']
                TianJinAllLocation.append(villageName)
                if  '社区居委会' in villageName:
                   TianJinAllLocation.append(villageName[:-5])
                if  '虚拟生活区' in villageName:
                    TianJinAllLocation.append(villageName[:-5])
                elif '村委会' in villageName:
                    if(villageName[-4] == '村'): #如果是 “村村委会”就去三个字“村委会”保留村
                        TianJinAllLocation.append(villageName[:-3])
                    else:                         #否则去两个字保留“村”
                        TianJinAllLocation.append(villageName[:-2])
                elif '居委会' in villageName:
                    TianJinAllLocation.append(villageName[:-3])
                elif '虚拟社区' in villageName:
                    TianJinAllLocation.append(villageName[:-4])
                elif '社区' in villageName:
                    TianJinAllLocation.append(villageName[:-2])
                else : continue
    return lists
p = provincetr(u=url, he=header, lists={})
#print('省')
c = citytr(u=url, he=header, lists=p)
#print('市')
o = countytr(u=url, he=header, lists=c)
#print('县')
t = towntr(u=url, he=header, lists=o)
#print('镇')
v = villagetr(u=url, he=header, lists=t)
#print('村')

with codecs.open("userdict.txt","a",'utf-8') as f:#格式化字符串还能这么用！
        for i in TianJinAllLocation:
            f.writelines(i + ' ' + 'ns' + '\r\n')
         #   f.write("\n")

