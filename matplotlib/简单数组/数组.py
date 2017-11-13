import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'
y = np.arange(50).tolist()
x = np.arange(50).tolist()
plt.plot(x, y )
plt.ylabel("test")
plt.xlabel("index")
plt.title("测试")
plt.axis([0,10,0,10])
plt.savefig("array", dpi=700)
plt.show()