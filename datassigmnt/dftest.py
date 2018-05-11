import pandas as pd
import datetime
import calendar as cal
import tushare as ts

def get_lastday_by_year(year):
    lastday = cal.monthrange(year, 12)
    lday = lastday[1]
    #print(lastday)
    day = datetime.date(year, 12, lday)
    #如果是今年的最后一天，设置为今天
    if day> datetime.date.today():
        day = datetime.date.today() + datetime.timedelta(seconds = -1)
    return day.strftime('%Y-%m-%d')

def test1():
	df = pd.DataFrame(columns=['year','c_name',"values"])
	indct = {"工业":['1','2'],"农业":['4','5'],"机械":[]}
	for k in indct.keys():
		tmp = pd.DataFrame({'year':range(2015,2018),"c_name":pd.Series(k,index=list(range(3))),"values":pd.Series(0,index=list(range(3)),dtype=int)})
		if df.empty:
			df = tmp
		else:
			df= df.append(tmp, ignore_index=True)

	for _, item in df.iterrows():
		print( item['year'], item['c_name'], item['values'])

def t_basic():
    day = datetime.date(2016, 12, 30) + datetime.timedelta(days=1)
    while True:
        sdate = day.strftime('%Y-%m-%d')
        print(sdate)
        try:
            val = ts.get_stock_basics(sdate)
            if val is None:
                day = day + datetime.timedelta(days=1)
            else:
                break
        except:
            day = day + datetime.timedelta(days=1)

#print( get_lastday_by_year(2018))
t_basic()