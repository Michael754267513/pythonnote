# encoding: utf-8
import re
import sys
try:
    f1 = open(sys.argv[1])
except IndexError:
    print "需要指定一个文件"
except IOError:
    print "请输入正确的文件"
else:
    C1 = 0
    for line in f1:
        for l1 in line.split():
            Nu1 = re.findall(r'^[a-zA-Z]+', l1)
            Nu = Nu1.__len__()
            if Nu == 1:
                if len(l1) == len(Nu1[0]):
                    C1 += Nu
    f1.close()
    print C1
