#encoding: utf-8
import ConfigParser

cf = ConfigParser.ConfigParser()
'''读取配置文件'''
cf.read("G:\code\config\config.txt")

'''读取文件配置,设置变量'''
jenkins_url = cf.get("config","jenkins_url")
username = cf.get("config","username")
password = cf.get("config","password")

