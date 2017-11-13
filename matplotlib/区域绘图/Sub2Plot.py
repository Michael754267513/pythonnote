import matplotlib.pyplot as plt
import numpy as np

a = np.arange(10)
#  (mxn) 横向m 纵向n mxn 的图形区块  (mxn) 从0 开始第m个横向第m个，纵向n个开始绘图
plt.subplot2grid((3,3),(0, 0))
plt.plot(a, a)
plt.subplot2grid((3,3),(0, 1),colspan=2)
plt.plot(a, a)
plt.subplot2grid((3,3),(1, 0),colspan=2)
plt.plot(a, a)
plt.subplot2grid((3,3),(1,2),rowspan=2 )
plt.plot(a, a)
plt.subplot2grid((3,3),(2, 0),colspan=2)
plt.plot(a, a)
plt.plot(a, a)
plt.show()