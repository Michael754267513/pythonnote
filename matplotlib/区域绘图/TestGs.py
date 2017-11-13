import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

a = np.arange(10)
gs = gridspec.GridSpec(3,3)
plt.subplot(gs[0:,1])
plt.plot(a, a)
plt.show()