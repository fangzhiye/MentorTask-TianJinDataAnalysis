# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 11:02:30 2018

@author: King
"""

import jieba
import jieba.posseg as posseg
import os
import pandas as pd
import sys
from datetime import datetime

def main():
    currentDir = os.path.abspath('.')
    userDictFile = os.path.join(currentDir,'userdict.txt')
    jieba.load_userdict(userDictFile)
    df = pd.read_csv("./processedtimeandlocation.csv")
   # df.drop(df.columns[-1], axis=1,inplace=True)
    m = df.shape[0]#获得DataFrame 只要.shape即可
    n = df.shape[1]#.shape 会获得一turple [0]为行 [1]为列
    # locationDF = pd.DataFrame({ '地点' : ''})
    # locationDF = ['地点']
    #df['去除地点和时间的句子'] = None
    #df['时间'] = None #增加新的一列，只要df['列名']即可 ，可以初始化为None
    #content = df['内容摘要']#获取一列数据为 df['列名']
    content = df['去除地点和时间的句子']
    segmentationContent = []
   # Dates = []
   # leftStrs = []
   # pattern = re.compile(r'([12]?[0-9]?[0-9]{1}[0-9]{1}[-/\.年])?([0-1]?[0-9]{1}[-/\.月][份]?)?([0-3]?[0-9]{1}[-/\.日]?)?([每天]?[早上]?[上午]?[中午]?[晚上]?[时]?)([\s])*([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')
    #pattern = re.compile(r'([0-9]{4}[-/\.年])?([0-1]?[0-9]{1}[-/\.月])?([0-3]?[0-9]{1}[-/\.日]?)?([\s])*([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')#定义匹配模式
   # pattern = re.compile(r'([0-9]{4}[-/\.年])*([0-1]?[0-9]{1}[-/\.月])+([0-3]?[0-9]{1}[-/\.日]?)([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')#定义匹配模式
    #jieba.add_word("年 t")  
    for i in range(m):
        string = content[i]
        seg = posseg.cut(string)
        sentence = []
        for w in seg:
            if(w.flag != 'x' and w.word !=' '):
              sentence.append(w.word) 
        segmentationContent.append(' '.join(sentence))


    #df.loc[:,'时间'] = Dates #设置某个元素的值为df.loc[行,列] = 值，其实也可以 = array
    #df.to_csv('所有处理过时间的投诉2018-3-29new.csv') #保存到csv 可以to_csv()
    #print(finalAddress)
    #print('/n')
    #print(l)

'''
在python编译器读取源文件的时候会执行它找到的所有代码，而在执行前会
根据当前运行的模块是否为主程序而定义变量__name__的值为__main__还是模
块名，而不是非主程序所引用的一个模块，如果你想要运行一些只有将在模块运行
而非当做模块引用进才执行的命令，只要放至__name__ = '__main__'之后即可
'''    
if __name__ == '__main__':
    main()