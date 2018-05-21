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
import re
from datetime import datetime

def main():
    currentDir = os.path.abspath('.')
    userDictFile = os.path.join(currentDir,'userdict.txt')
    jieba.load_userdict(userDictFile)
    df = pd.read_csv("firstStepProcessLocation.csv")
    df.drop(df.columns[-1], axis=1,inplace=True)
    m = df.shape[0]#获得DataFrame 只要.shape即可
    n = df.shape[1]#.shape 会获得一turple [0]为行 [1]为列
    # locationDF = pd.DataFrame({ '地点' : ''})
    # locationDF = ['地点']
    df['去除地点和时间的句子'] = None
    df['时间'] = None #增加新的一列，只要df['列名']即可 ，可以初始化为None
    #content = df['内容摘要']#获取一列数据为 df['列名']
    content = df['提取地点后的句子']
    Dates = []
    leftStrs = []
   # pattern = re.compile(r'([12]?[0-9]?[0-9]{1}[0-9]{1}[-/\.年])?([0-1]?[0-9]{1}[-/\.月][份]?)?([0-3]?[0-9]{1}[-/\.日]?)?([每天]?[早上]?[上午]?[中午]?[晚上]?[时]?)([\s])*([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')
    #pattern = re.compile(r'([0-9]{4}[-/\.年])?([0-1]?[0-9]{1}[-/\.月])?([0-3]?[0-9]{1}[-/\.日]?)?([\s])*([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')#定义匹配模式
   # pattern = re.compile(r'([0-9]{4}[-/\.年])*([0-1]?[0-9]{1}[-/\.月])+([0-3]?[0-9]{1}[-/\.日]?)([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')#定义匹配模式
    #jieba.add_word("年 t")  
    for i in range(m):
        string = content[i]
        #string = '举报出租：车牌号：津E01716 拒载时间：2017年3月24日8:40 地点：下面 市民表示司机停车后市民走到副驾驶的位置，什么都没说司机就要开走，市民拍了下车，司机下车后态度非常恶劣，特此举报。望相关部门核实处理。（匿名举报）'
        date_all = re.findall(pattern,string)
        date_all.sort()
        #finalTime = ' '
       # finalTime = ''.join(date_all[-1])
        '''
        minNone = 10000
        Index = -1
        for i in range(0, date_all.__len__())[::-1]:
#for i in range(numItems):
           numNone = date_all[i].count('')
           if numNone < minNone:
               minNone = numNone
               Index = i
        if Index != -1:       
            finalTime= ''.join(date_all[Index])
        '''
       # for item in date_all:
       ###     if item and item !=' ':
        finalTime = ''.join(date_all[-1])
                
        if len(finalTime) > 4:
            leftStrs.append(string.replace(finalTime,''))
        else: leftStrs.append(string)
        
        if  finalTime == ' ' :
            Dates.append(finalTime)
        elif len(finalTime) > 4:
            Dates.append(finalTime.lstrip())
        else:
            Dates.append(' ')
        #string = '消费维权，2017年3月24日在南开区华苑路106号华苑第八小区商业中心第一层一室的嘉和一品用餐，在老北京扣肉饭中吃出了一个锐利硬塑料异物，市民认为该店食品卫生存在隐患，故来电举报希望相关部门对其进行监察。	'
       # print(string)
        #string = '2017年3月24日市民反映：北辰区大张庄镇北河庄村村长方贵坡，在村内盖了五层的楼房，'
       #遮挡其他村民房子的阳光，按照规定是村内不允许盖楼房的，希望相关部门核实处理。反映人未留姓氏'
        '''
        seg = list(posseg.cut(string))  
        #    print(type(seg))
        l = []
        time = []
        finalTime = ''
        firstIndex = -1
        lastIndex = -1
        segLength = len(seg)
        #indexCount = 0
        for i, element in enumerate(seg):
            #indexCount = indexCount + 1
            l.append((element.word,element.flag)) 
            
            if(element.flag == 'm' or element.flag == 't' ):
                if(firstIndex == -1):
                    firstIndex = i
                  #  print('firstIndex: %d'%(firstIndex))
                lastIndex = i
               # print('lastIndex: %d'%(lastIndex))
            if(element.flag == 'x' and lastIndex > firstIndex ):
                break
        
        
        nsLength = lastIndex - firstIndex + 1
        #if nsLength/segLength < 0.5:
        for i in range(firstIndex, lastIndex + 1):
            if(seg[i].flag == 'x'):
                break
            elif (seg[i].flag != 'p' and seg[i].flag != 'v'):
                time.append(seg[i].word)
                #if(element.word not in address):
                    #address.append(element.word)
         #  print(address)
         ''' 
         #print(l)
         #finalTime= ''.join(time)  #将数组Array转成字符串
         #Dates.append(finalTime)
    print(Dates)
    df.loc[:,'去除地点和时间的句子'] = leftStrs
    df.loc[:,'时间'] = Dates #设置某个元素的值为df.loc[行,列] = 值，其实也可以 = array
    df.to_csv('所有处理过时间的投诉2018-3-29new.csv') #保存到csv 可以to_csv()
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