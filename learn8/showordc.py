'''
显示词云
'''
#coding:utf-8
import matplotlib.pyplot as plt
import wordc

def ShowWcld():
    wg = wordc.WordGenrt()
    plt.imshow(wg,interpolation='bilinear')
    plt.axis('off')
    plt.show()

ShowWcld()