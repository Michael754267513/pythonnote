#!/usr/bin/env python
# coding=utf8


import sys
import MySQLdb
import MySQLdb.cursors


class MySQLUserProcess:
    def __init__(self, **kwargs):
        """Initialize"""
        self.connection_options = {}
        self.connection_options['user'] = 'root'
        self.connection_options['passwd'] = kwargs['password']
        self.connection_options['host'] = kwargs['ip_address']
        self.connection_options['port'] = 3306
        # self.connection_options['database'] = 'mysql'
        self.connection_options['cursorclass'] = MySQLdb.cursors.DictCursor
        self.connect()

    def connect(self):
        try:
            # 打开数据库连接
            self.db = MySQLdb.connect(**self.connection_options)
        except Exception, e:
            raise Exception, "Cannot interface with MySQL server, %s" % e

    def query(self, statement):
        try:
            # 使用cursor()方法获取操作游标
            cursor = self.db.cursor()
            # 执行SQL语句
            cursor.execute(statement)
            data = cursor.fetchall()
            return data
        except Exception, e:
            print e
        # 关闭数据库
        self.db.close()

    def statement_execute(self, statement):
        try:
            # 使用cursor()方法获取操作游标
            cursor = self.db.cursor()
            # 执行SQL语句
            cursor.execute(statement)
            # 提交到数据库执行
            self.db.commit()
        except Exception, e:
            # 失败回滚
            self.db.rollback()
            print e

        self.db.close()

    def get_version(self):
        statement = "select version()"
        return self.query(statement)

    def get_mysql_users(self):
        statement = """select Host,User from mysql.user"""
        return self.query(statement)

    def add_user(self, username, hostname, password):
        statement = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s'" % (username, hostname, password)
        print statement
        if self.statement_execute(statement) is None:
            return True

    def privileges_process(self, privilege_name, dbname, username, hostname):
        statement = "grant %s on %s.* to %s@'%s'" % (privilege_name, dbname, username, hostname)
        print statement
        if self.statement_execute(statement) is None:
            return True

    def del_user(self, user, host):
        statement = "DROP USER '%s'@'%s'" % (user, host)
        if self.statement_execute(statement) is None:
            return True

    def reset_password(self, username, hostname, password):
        # statement = "UPDATE mysql.user SET Password = PASSWORD('%s') WHERE user = '%s'" % (newpasswd, user)
        statement = "ALTER USER '%s'@'%s' IDENTIFIED BY '%s'" % (username, hostname, password)   # 5.7.6 or later
        # statement = "SET PASSWORD FOR '%s'@'%s' = PASSWORD('%s')"  # 5.7.5 and earlier
        if self.statement_execute(statement) is None:
            return True


def use_age():
    """Display program useage"""
    print "Usage : ", sys.argv[0], "function"
    print "function: get_version get_mysql_users add_user privileges_process del_user reset_password"
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        use_age()
