import pandas as pd

df = pd.DataFrame(columns=['year','c_name',"values"])
indct = {"工业":['1','2'],"农业":['4','5'],"机械":[]}
for k in indct.keys():
	tmp = pd.DataFrame({'year':range(2015,2018),"c_name":pd.Series(k,index=list(range(3))),"values":pd.Series(0,index=list(range(3)),dtype=int)})
	if df.empty:
		df = tmp
	else:
		df= df.append(tmp, ignore_index=True)