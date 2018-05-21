import re
from datetime import datetime
pattern = re.compile(r'([12]?[0-9]?[0-9]{1}[0-9]{1}[-/\.年])?([0-1]?[0-9]{1}[-/\.月][份]?)?([0-3]?[0-9]{1}[-/\.日]?)?([每天]?[早上]?[上午]?[中午]?[晚上]?[时]?)([\s])*([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')
#pattern = re.compile(r'([0-9]{2,4}[-/\.年])?([0-1]?[0-9]{1}[-/\.月][份]?)?([0-3]?[0-9]{1}[-/\.日]?)?([每天]?[早上]?[上午]?[中午]?[晚上]?[时]?)([\s])*([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')#定义匹配模式
#pattern = re.compile(r'([0-9]{4})[-/\.年]([0-1]?[0-9]{1})[-/\.月]([0-3]?[0-9]{1})[日]([0-2]?[0-9](:[0-6][0-9]){2})?')#定义匹配模式
#pattern = re.compile(r'([0-9]{4})[-/\.年]([0-1]?[0-9]{1})[-/\.月][日](\d{1,2}:\d{1,2})')#定义匹配模式
string = '市民反映：投诉101号(福安大街口)的桂顺斋，于2017年3月24日购买白皮托盘，花费95.3元，没有给小票。市民不认可，诉求：希望赔偿。'
date_all = re.findall(pattern,string)
date_all.sort()
#mat = re.search(pattern,string)
#print(mat)
#final = ''
numItems = len(date_all)
minNone = 10000
Index = -1
for i in range(0, date_all.__len__())[::-1]:
#for i in range(numItems):
    numNone = date_all[i].count('')
    if numNone < minNone:
        minNone = numNone
        Index = i
if Index != -1:       
    final= ''.join(date_all[Index])
final = ''.join(date_all[Index])
print(final)
