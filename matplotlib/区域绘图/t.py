import matplotlib.pyplot as plt
import numpy as np

a = np.arange(1,100)
y = np.sin(np.pi * (a / 100))
plt.subplot(3,2,1) # 绘制 3x2 的形状选取第一个
plt.plot(a.tolist(), y.tolist())
plt.xlabel("无敌", fontproperties='SimHei',fontsize=20)
plt.subplot(3,2,4) # 回执3x2 的形状在第四个绘制
plt.plot([1,2,3,4])
plt.show()