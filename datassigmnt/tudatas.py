import tushare as ts
import pandas as pd
import datetime

'''
 按行业分类 和概念分类 
 统计按行业、按概念在近5年的总的估值变化
'''

def industrydata():
    indls = ts.get_industry_classified()
    indct = dict()
    for _,row in indls.iterrows():
        try:
            tmp= indct.get(row['c_name'],[])
            tmp.append(row['code'])
            indct[row['c_name']] = tmp
        except:
            pass

    return indct

def get_stock_value(code):
    pass

def get_industry_value(indct, n):
    y = datetime.date.year
    #cols = ['c_name','values','count']
    indvalue = pd.DataFrame()
    for k in indct.keys():
        tmp =  pd.DataFrame({'year':range(y-n+1,y+1),
                             'c_name':k,
                             'values':pd.Series(0, index=list(range(n)), dtype=float),
                             'count': pd.Series(0, index=list(range(n)),dtype=int)})
        indvalue.append( tmp)
    for k,v in indct.items():
        for code in set(v):
            get_stock_value(code)
    pass

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
    indvalue = get_industry_value(indct)

    conceptdata()
    #按概念化的变化
    convalue= get_concept_value()