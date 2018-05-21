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
def writeToTxt(list_name,file_path):
    try:
        fp = open(file_path,"w+")
        for item in list_name:
            fp.write(str(item)+"\n")
        fp.close()
    except IOError:
        print("fail to open file")
        
def main():
    currentDir = os.path.abspath('.')
    userDictFile = os.path.join(currentDir,'userdict.txt')
    jieba.load_userdict(userDictFile)
    df = pd.read_excel("AllData.xlsx")
    df.drop(df.columns[-1], axis=1,inplace=True)
    m = df.shape[0]#获得DataFrame 只要.shape即可
    n = df.shape[1]#.shape 会获得一turple [0]为行 [1]为列
    # locationDF = pd.DataFrame({ '地点' : ''})
    # locationDF = ['地点']
    df['提取地点后的句子'] = None
    df['地点'] = None #增加新的一列，只要df['列名']即可 ，可以初始化为None
    df['提取地点后的句子'] = None
    content = df['内容摘要']#获取一列数据为 df['列名']
    locations = []
    leftStrs = []
    for i in range(m):
        string = content[i]
        #string = '投诉出租 津E00616,2017年3月24日22:20左右，在南京路吉利大厦打算去南开大学，上车后司机询问去向拒载，来电投诉司机拒载。（市民匿名反映，不需要回复。）'
       # print(string)
       #string = '市民反映：北辰区大张庄镇北河庄村村长方贵坡，在村内盖了五层的楼房，
       #遮挡其他村民房子的阳光，按照规定是村内不允许盖楼房的，希望相关部门核实处理。反映人未留姓氏'
        seg = list(posseg.cut(string))  
    #    print(type(seg))
        l = []
        address = []
        addressIndex = []
        finalAddress = ''
        firstIndex = -1
        lastIndex = -1
        segLength = len(seg)
        leftStr = []
        #indexCount = 0
        for i, element in enumerate(seg):
            #indexCount = indexCount + 1
            l.append((element.word,element.flag))      
            if(element.flag == 'ns' or element.flag == 'nt' ):
                if(firstIndex == -1):
                    firstIndex = i
                  #  print('firstIndex: %d'%(firstIndex))
                lastIndex = i
               # print('lastIndex: %d'%(lastIndex))
            if(element.flag == 'x' and lastIndex > firstIndex ):
                break
        nsLength = lastIndex - firstIndex + 1
        #if nsLength/segLength < 0.5:
      #  for i, element in enumerate(seg):
            

        for i in range(firstIndex, lastIndex + 1):
            if(seg[i].flag == 'x'):
                break
            elif (seg[i].flag != 'p' and seg[i].flag != 'v'):
               # address.append(seg[i].word)
                addressIndex.append(i)
                #if(element.word not in address):
                    #address.append(element.word)
         #  print(address)
       # print(l)
        for i, element in enumerate(seg):
           if i in addressIndex:
               address.append(element.word)
           else:
               leftStr.append(element.word)
        finalAddress= ''.join(address)  #将数组Array转成字符串
        leftStrs.append(''.join(leftStr))
        locations.append(finalAddress)
       # print(locations)
    df.loc[:,'提取地点后的句子'] = leftStrs
    df.loc[:,'地点'] = locations #设置某个元素的值为df.loc[行,列] = 值，其实也可以 = array
    df.save('firstStep2018-3-29.xlsx') #保存到csv 可以to_csv()
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