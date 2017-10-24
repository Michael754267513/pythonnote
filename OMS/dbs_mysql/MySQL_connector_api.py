#!/usr/bin/env python
# coding=utf8

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor import MySQLCursorDict
import sys


class MySQLUserOperate:

    def __init__(self, **kwargs):
        """Initialize"""
        self.connection_options = {}
        self.connection_options['user'] = 'root'
        self.connection_options['password'] = kwargs['password']
        self.connection_options['host'] = kwargs['ip_address']
        self.connection_options['database'] = 'mysql'
        self.connection_options['raise_on_warnings'] = True
        self.connection_options['use_unicode'] = False
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.connection_options)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Acess denied/wrong  user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)

    def query(self, statement):
        cursor = MySQLCursorDict(self.conn)
        cursor.execute(statement)
        result = cursor.fetchall()
        cursor.close()
        return result

    def statement_execute(self, statement):
        cursor = MySQLCursor(self.conn)
        cursor.execute(statement)
        cursor.close()

    def get_version(self):
        statement = "select version()"
        return self.query(statement)

    def get_mysql_users(self):
        statement = "select Host,User,password_last_changed from user"
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

def useage():
    """Display program useage"""
    print "Usage : ", sys.argv[0], "function"
    print "function: get_version get_mysql_users add_user privileges_process del_user reset_password"
    sys.exit(1)

if __name__ == '__main__':
    # fun_list = ('get_version', 'get_mysql_users', 'add_user', 'privileges_process', 'del_user', 'reset_password')
    if len(sys.argv) != 2:
        useage()
        # process = MySQLUserOperate()
        # print process.get_version()
        # for row in process.get_mysql_users():
        #     print row
        # print process.add_user('jack', '%', 'leshu@1688KW')
        # print process.del_user('jack', '%')
        # print process.privileges_process('select', 'OMS', 'jack', '%')
        # print process.reset_password('jack', '%', 'Luckyzhou@1688')
    # else:
    #     useage()
