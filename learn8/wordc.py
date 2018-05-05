'''
 词云处理
'''
#coding:utf-8
import wordcloud
import splitword
import readimg



def WordGenrt():
    #词云使用msyh.ttc 字体
    msk = readimg.ReadBKImg('../resources/ksy.jpg','im')
    w = wordcloud.WordCloud(font_path='MSYH.TTC',max_words=30,mask=msk,\
                            background_color='white')
    txt = splitword.SplitWords(u"../resources/新时代中国特色社会主义.txt")
    return w.generate(txt)

def main():
    wg = WordGenrt()
    wg.to_file('cs.png')


if __name__ == '__main__':
    main()