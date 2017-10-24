# encoding: utf-8
import re

list1 = '''420984199111257412L 750 -750 750.131 -750.131 michael
 QQ754267513 Name michael_jack password 曾浩
754267513@qq.com  http://www.baidu.com  15071314780
1507-1314780 <http://www.example/com>'''
print re.findall(r'\d{15}|\d{18}', list1)
print re.findall(r'\d+', list1)
print re.findall(r'\s', list1)
print re.findall(r'\A', list1)
print re.findall(r'\Z', list1)
print re.findall(r'\b', list1)
