from pylab import *
x1 = range(0, 20)
y1 = [x for x in x1]
y2 = [7/2 - 3/2 * x for x in x1]
# 划线
plot(x1, y1, linewidth=1,)
plot(x1, y2, linewidth=1)
# 横抽标签
xlabel('x')
# 纵抽标签
ylabel('y')
# 标题
title("this is example")
grid(True)
show()