import sys
fp = open('test.txt','rb')
fp.readline()
fp.seek(10,1)
print(fp.readline())
