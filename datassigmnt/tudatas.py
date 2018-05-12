#tudatas.py
import tushare as ts
import pandas as pd
import datetime
import math
import calendar as cal
import matplotlib.pyplot as plt


def classified_data(type='industry'):
    '''
    按行业分类分类统计按行业、季度近5年的总的估值变化 , 以字典的形式返回分类数据信息
    :param type: 类型，默认为工业企业
    :return:
     {"工业企业":['600001','600002']}
      分类： 对应的企业代码集合
    '''
    if type   == 'industry':
        indls = ts.get_industry_classified()
    elif type == 'concept':
        indls = ts.get_concept_classified()
    print("获取分类数据成功")
    indct = dict()
    for _,row in indls.iterrows():
        try:
            tmp= indct.get(row['c_name'],[])
            tmp.append(row['code'])
            indct[row['c_name']] = tmp
        except:
            pass
    return indct


def try_nextday_basics(sday, itry=7):
    '''
    获取企业总资产，默认向后试7天
    :param sday: 获取指定的天数的资产情况
    :param itry: 默认重试7天
    :return: 返回获取的总估计列表，DataFrame类型
    '''
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


def get_stock_value(yearq):
    '''
    获取指定季度的估值，转换为指定的某天
    :param yearq: 季度 如 2017Q1
    :return: 总值的DataFrame
    '''
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

def build_cloumns(indct):
    '''
    根据分类动态沟通 columns
    :param indct: 按行业分类字典
    :return: columns 列表
    '''
    cols = []
    for k in indct.keys():
        cols.append(k)
    return cols


def build_industry_frame(indct):
    '''
    # get_stock_basics 数据只从 2016-8-9 开始 , 截止到今天
    创建 DataFrame数据集
    :param indct:
    :return:
    columns: index , GY,      ZH,    SY , ...
     2016Q3      33333     44444  555
    '''
    start = '2016-08-09'
    end = datetime.date.today().strftime('%Y-%m-%d')
    #当前年2018 , 按季度 总资产 的变化 [2016Q3, 2016Q4]  --> index=pr
    pr = pd.period_range(start=start,end=end, freq='Q')
    #构建 columns , 记录对应的columns对应关系，不使用中文column
    cols = build_cloumns(indct)
    indvalue = pd.DataFrame(index=pr, columns=cols)
    return indvalue

def handle_datas(codes, stocks):
    '''
    查询按行业分类企业的总资产值
    :param codes: 企业代码列表 如['600001','600002']
    :param stocks: 指定总的资产的DataFrame
    :return: 总值
    '''
    q = 'code == %s'%codes
    try:
        return stocks.query(q)['totalAssets'].sum()
    except:
        return 0.0

def get_industry_value( indct):
    '''
    按行业获取对应的值
    :param indct: 行业分类字典
    :return: 返回的DataFrame
    '''
    indvalues = build_industry_frame(indct)
    #print(indvalues)
    print("创建按季度分析数据集成功")
    #需处理的记录总数， 每季度的 Q1,Q2 * 工业，机械等行业
    total = indvalues.shape[0] * len(indct)
    #print(icount)
    icount = 1
    for index,item in indvalues.iterrows():
        yearq = str( index)
        #按季度读取总值
        total_values = get_stock_value(yearq)
        for k,v in indct.items():
            indvalues[k][index] = handle_datas(v, total_values)
            # print("获取【%s-%s】分类股票总值成功"%(item['c_name'],yearq))
            #处理的进度情况  --TODO 文本进度条
            c = (icount/total)*100
            print("获取数据进度为:{:.2f}%".format(c))
            icount +=1
    #print(indvalues)
    return indvalues

def parse_show( indvalue):
    '''
    处理并展现数据
    :param indvalue: DataFrame
    :return:
    '''
    #将数量级相同的放到一个界面显示
    #print( indvalue)
    cols = indvalue.columns.values.tolist()

    indvalue[cols] = indvalue[cols].astype('float64')
    print(indvalue)

    shdic = dict()
    for _,item in indvalue.iterrows():
        for c in cols:
            s = '%e'%item[c]
            if len(s)>1:
                sv = int( s[s.index('+')+1: len(s)])
                ret = shdic.get(sv, [])
                ret.append(c)
                shdic[sv] = ret
        #只需要判断第一行数量级即可
        break

    for value in shdic.values():
        ilen =  math.ceil(len(value)/5)
        for ipos in range(ilen):
            start = ipos *5
            end = (ipos +1)*5
            if end > len(value):
                end = len(value)
            indvalue[value[start: end]].plot()
    plt.show()


def main():
    indct = classified_data()
    #取按工业化的数据变化
    #print(indct)
    print("生成工业分类字典成功")
    indvalue = get_industry_value(indct)
    #print(indvalue)
    parse_show( indvalue)


if __name__ == '__main__':
    main()