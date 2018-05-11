import pymysql
#coding:utf-8
import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=8083, user='phstest', passwd='phstest@20161205', db='g_lb', charset='utf8')
# 创建游标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 执行SQL，并返回收影响行数

# 执行SQL，并返回受影响行数
# effect_row = cursor.execute("update tb7 set pass = '123' where nid = %s", (11,))
# 执行SQL，并返回受影响行数,执行多次
# effect_row = cursor.executemany("insert into tb7(user,pass,licnese)values(%s,%s,%s)", [("u1","u1pass","11111"),("u2","u2pass","22222")])
#cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute("select xm,csrq,jtdz7,lxdh from da_grda0 limit 10")
row1 = cursor.fetchall()
print(row1)
# 关闭游标
cursor.close()
# 关闭连接
conn.close()