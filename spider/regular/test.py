#!encoding: utf-8
import re
# regular 常用字符
secret_code = 'asdadxxaaxxasdasdsdxxbbxxasdasdsxxccxxasdad'

print re.findall("xx.", secret_code)
print re.findall("xx*", secret_code)
print re.findall("xx.*xx", secret_code)
print re.findall("xx.*?xx", secret_code)
print re.findall("xx(.*?)xx", secret_code)

test_code = '''asdasdxxaa
xxbbxxasdxxccxx'''
print re.findall("xx(.*?)xx", test_code, re.S)
print re.findall("xx(.*?)xx(.*?)xx", secret_code)
print re.sub("xx(.*?)xx", test_code, "laoshu")
print re.search("xx(.*?)xx", test_code, re.S)