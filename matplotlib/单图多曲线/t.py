import matplotlib.pyplot as plt
import numpy as np
xlab = np.arange(20)
plt.plot(xlab,xlab*2,'bx-' ,xlab,xlab/2,'bx-')
plt.show()