'''
读取背景图片
'''
#coding:utf-8
import numpy as np
from PIL import Image
from scipy.misc import imread

def ReadBKImgbyNP(img):
    return np.array( Image.open(img))

def ReadBKImgbyIm(img):
    return imread(img)

def ReadBKImg(img, type):
    if type=='im':
        return ReadBKImgbyIm(img)
    else:
        return ReadBKImgbyNP(img)