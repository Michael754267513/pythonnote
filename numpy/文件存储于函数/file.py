import numpy as np

a = np.arange(100).reshape(2, 50)
print(a)
#### savetxt  loadtxt 只能读取一维和二维数组 保留格式
np.savetxt("save.txt", a, delimiter=',', fmt='%.2f')
afile = np.loadtxt('save.txt', dtype=np.float, delimiter=',', unpack=False)
print(afile)
##### 多维数据存储不会存储数组的维度  - 需要额外的保存 然后进行reshape
b = np.arange(100).reshape(2, 5, 10)
print(b)
b.tofile("filetotxt", sep=",", format='%d')
b.tofile("filetotxt1", format='%d')
bb = np.fromfile("filetotxt", dtype=np.int, count=-1, sep=",")
print(bb)
print("--------------------------------------")
bb1 =  np.fromfile("filetotxt1", dtype=np.int)
print(bb1)

###############3 文件存储 savez 进行压缩   会保存原来的数组信息，
a = np.arange(100).reshape(2, 5, 10)
np.save("savefile", a)
print(np.load("savefile.npy"))
#