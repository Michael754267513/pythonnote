from pylab import *
t = arange(0.0, 2.0, 0.01)
s = sin(2 * pi * t)
# 划线
plot(t, s, linewidth=1.0)
# 横抽标签
xlabel('time(s)')
# 纵抽标签
ylabel('vol(mv)')
# 标题
title("this is example")
grid(True)
show()