import tushare as ts
import pandas as pd
import datetime
import time
import calendar as cal

'''
 按行业分类 和概念分类 
 统计按行业、按概念在近5年的总的估值变化
'''

def industrydata():
    indls = ts.get_industry_classified()
    print("获取工业分类数据成功")
    indct = dict()
    for _,row in indls.iterrows():
        try:
            tmp= indct.get(row['c_name'],[])
            tmp.append(row['code'])
            indct[row['c_name']] = tmp
        except:
            pass
    return indct

'''
取指定年的最后一天，如果是当前日期，去昨天的记录
'''
def get_lastday_by_year(year):
    lastday = cal.monthrange(year, 12)
    day = datetime.date(year, 12, lastday[1])
    #如果是今年的最后一天，设置为今天
    if day> datetime.date.today():
        day = datetime.date.today() + datetime.timedelta(seconds = -1)
    return day.strftime('%Y-%m-%d')

def try_nextday_basics(sday, itry=7):
    day = datetime.datetime.strptime(sday,'%Y-%m-%d').date()
    #不超过当前日期
    if day > datetime.date.today():
        day = datetime.date.today() + datetime.timedelta(seconds=-1)
    k =0
    while True:
        sdate = day.strftime('%Y-%m-%d')
        try:
            val = ts.get_stock_basics(sdate)
            if val is None:
                day = day + datetime.timedelta(days=1)
                k += 1
                if k > itry:
                    return None
                #print("尝试：%d, 日期：%s"%(k, sdate))
            else:
                #print("获取日期：%s数据" %sdate)
                return val
        except:
            day = day + datetime.timedelta(days=1)

'''
获取对应年份的股票的市值
每年的股票数可能不太相同，需要根据返回的数据判断是否有市值
get_stock_basics 只能获取到 2016-8-9的数据，其他的数据不能
'''
def get_stock_value(yearq):
    #取year最后一天的市值
    v = yearq[-1]
    if v== '1':
        d = '-03-31'
    elif v== '2':
        d = '-06-30'
    elif v == '3':
        d = '-09-30'
    else:
        d = '-12-31'
    sdate = yearq[0:4] + d
    #有可能刚好当天的数据不存在，向下找7天，如果没有就返回 None
    return try_nextday_basics( sdate)

'''
  创建 DataFrame数据集
'''
def build_industry_frame(indct):
    # get_stock_basics 数据只从 2016-8-9 开始
    start = '2016-08-09'
    end = datetime.date.today().strftime('%Y-%m-%d')
    #当前年2018 , 按季度 总资产 的变化
    pr = pd.period_range(start=start,end=end, freq='Q')
    indvalue = pd.DataFrame(columns=['yearq', 'c_name', 'values', 'count'])
    for k in indct.keys():
        tmp = pd.DataFrame({'yearq': pr,
                            'c_name': k,
                            'values': 0.0,
                            'count': 0})
        indvalue = indvalue.append(tmp, ignore_index=True)
    return indvalue

def handle_datas(codes, stocks):
    q = 'code == %s'%codes
    try:
        return stocks.query(q)['totalAssets'].sum()
    except:
        return 0

def get_industry_value( indct):
    indvalues = build_industry_frame(indct)
    #print(indvalues)
    print("创建按季度分析数据集成功")
    #按 行业的年读取数据 如 2016Q3 , 工业, codes:[]
    rcount = indvalues.shape[0]
    #print(rcount)
    k = 1
    for _,item in indvalues.iterrows():
        codes = indct.get( item['c_name'], None)
        if codes is not None:
            yearq = str(item['yearq'])
            item['values'] = handle_datas(codes, get_stock_value( yearq))
            item['count'] = len(set(codes))
            #print("获取【%s-%s】分类股票总值成功"%(item['c_name'],yearq))
        else:
            item['values'] = 0
            item['count']  = 0
        c = (k/rcount)*100
        print("获取数据进度为:{:.2f}%".format(c))
        k +=1
    return indvalues

def conceptdata():
    conls = ts.get_concept_classified()
    condct = dict()
    for _, row in conls.iterrows():
        try:
            tmp = condct.get(row['c_name'], [])
            tmp.append(row['code'])
            condct[row['c_name']] = tmp
        except:
            pass

    return condct

def get_concept_value(condct):
    pass

def main():
    indct = industrydata()
    #取按工业化的数据变化
    #print(indct)
    print("生成工业分类字典成功")
    indvalue = get_industry_value(indct)
    print(indvalue)
    #conceptdata()
    #按概念化的变化
    #convalue= get_concept_value()

def t1():
    print(build_industry_frame({"专用机械":[],"互联网":[]}))

if __name__ == '__main__':
    main()