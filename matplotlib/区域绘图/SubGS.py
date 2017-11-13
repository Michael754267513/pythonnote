import matplotlib.gridspec as gridspec
import matplotlib.pyplot as  plt

gs = gridspec.GridSpec(3,3)


#  数据切片一样，mxn 纵向M 切片  横向n切片
plt.subplot(gs[0,0])
plt.subplot(gs[0,1:])
plt.subplot(gs[1,:2])
plt.subplot(gs[1:,-1])
plt.subplot(gs[2,:2])
plt.show()