#encoding: utf-8
import MySQLdb


def select_mysql(sql):
    try:
        #打开数据库连接
        conn = MySQLdb.connect(host='192.168.12.171', user='root', passwd='root', db='devops', port=3306,
                               charset='utf8')
        #获取操作游标
        cur = conn.cursor()
        #执行sql语句
        cur.execute(sql)
        #获取全部数据
        data = cur.fetchall()
        #获取一条数据
        #data_one =cur.fetchone()
        #关闭游标
        cur.close()
        #关闭连接
        conn.close()
        return data
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def update_mysql(sql):
    try:
        conn = MySQLdb.connect(host='192.168.12.171', user='root', passwd='root', db='devops', port=3306,
                               charset='utf8')
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])