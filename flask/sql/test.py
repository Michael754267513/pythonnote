#encoding: utf-8
import MySQLdb

conn = MySQLdb.connect(host='192.168.12.171', user='root', passwd='root', db='devops', port=3306,
                               charset='utf8')
cur = conn.cursor()
cur.execute("select id,name,tel,mail from users")
#data1 = cur.fetchone()
data = cur.fetchall()
cur.close()
conn.close()
print data
