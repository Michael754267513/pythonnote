import matplotlib.pyplot as plt
import numpy as np

a = np.arange(10)
plt.xlabel("横坐标", fontproperties='SimHei',fontsize=15)
plt.ylabel("纵坐标",fontproperties='SimHei',fontsize=15)
plt.title("标签", fontproperties='SimHei',fontsize=20)
plt.text(5,5,"跳跳", fontproperties='SimHei',fontsize=15)
plt.annotate("文本",xy=(5,5),xytext=(4,7), fontproperties='SimHei',fontsize=10, arrowprops=dict(facecolor='black',shrink=0.1, width =2))# 箭头
plt.plot(a,a)
plt.axis([0,10,0,10])
plt.show()