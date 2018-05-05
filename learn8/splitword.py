'''
分词处理
'''
#coding:utf-8

import jieba

#分词后转为词云需要的字符列表
def SplitWords(fpath):
    f = open(fpath, 'r', encoding='utf-8')
    contents = f.read()
    f.close()
    ls = jieba.lcut(contents)
    return " ".join(ls)