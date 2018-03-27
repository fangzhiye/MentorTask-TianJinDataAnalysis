import re
from datetime import datetime
pattern = re.compile(r'([0-9]{4}[-/\.年])*([0-1]?[0-9]{1}[-/\.月])+([0-3]?[0-9]{1}[-/\.日]?)([0-2]?[0-9][点]?[:]?[0-6][0-9][分]?)?')#定义匹配模式
#pattern = re.compile(r'([0-9]{4})[-/\.年]([0-1]?[0-9]{1})[-/\.月]([0-3]?[0-9]{1})[日]([0-2]?[0-9](:[0-6][0-9]){2})?')#定义匹配模式
#pattern = re.compile(r'([0-9]{4})[-/\.年]([0-1]?[0-9]{1})[-/\.月][日](\d{1,2}:\d{1,2})')#定义匹配模式
string = '	市民来电：投诉津E29671的出租车，2017.12.24早晨10点半左右到11点左右，市民从金钟河大街公交站到津滨大道天津市恒森消防工程有限公司，收市民21元（包括燃油附加费），有小票，但是小票时间不对，金额也不对，市民无法报销，希望换成市民乘坐出租车的小票'
date_all = re.findall(pattern,string)
mat = re.search(pattern,string)
final = ''
for item in date_all:
    if item:
        final = ''.join(item)
print(final)