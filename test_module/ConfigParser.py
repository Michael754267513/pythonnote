#encoding: utf-8
import ConfigParser

cf = ConfigParser.ConfigParser()
'''读取配置文件'''
cf.read("G:\code\config\hosts")

'''读取文件配置,设置变量'''
jenkins_url = cf.get("web","web01")

'''获取机器分组列表'''
print  cf.sections()
'''列出匹配分类机器'''
print  cf.options("web")
'''获取选定分组机器对应的值'''
print cf.items("web")
'''获取单个分组的指定匹配机器相关值'''
print cf.get("web","web01")
''''''''''''''''''''''''''''''''''''
'''修改配置文件'''
cf.set("web","web01","1.1.1.3")
'''添加新的分组成员'''
cf.set("web","web03","1.1.1.4")
'''新增一个分组'''
#cf.add_section("db")
cf.set("db","db01","2.2.2.2")
'''保存修改'''
cf.write(open("G:\code\config\hosts","w"))