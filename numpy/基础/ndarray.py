import numpy as np
# 计算两个数组相加
a = [1, 2, 3, 4, 5]
b = [1, 2, 3, 4, 5]
c = []
for i in range(len(a)):
    c.append(a[i] + b[i])
print(c)
# np 计算两个数组相加，可以直接数据相加，无需for （NDarray）
np_a = np.array(a)
np_b = np.array(b)
print(np_a + np_b)

###########################
nd_a = np.array([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
print(nd_a.ndim) # 维度
print(nd_a.shape) # 表示是3 x 4 的矩阵
print(nd_a.size) # 大小
print(nd_a.dtype)# 类型
##########################
n = 10
m = 20
# print(np.arange(n, m)) # 生成一个连续数从n 到m -1
# print(sum(np.arange(0, 101))) # 计算1到100的和
# print(np.ones(shape=[n, m])) # 生成一个全部为1的数组，N X M 的全1矩阵
# print(np.zeros(shape=[n, m])) # 生成一个全部为0的数组，N X M 的全0矩阵
# print(np.full(shape=[n], fill_value=m)) # 生成n个m的数组
# print(np.eye(2, 2)) # 生成一个N X M 的标准矩阵，正对角线为1 ，其余为0 的标准矩阵

a = np.array([1, 2, 3, 4])
print(np.empty_like(a))
print(np.zeros_like(a))
print(np.ones_like(a))
print(np.full_like(a, fill_value=n))
#################################数组的合并
n = 1
m = 10
N = 4
print(np.linspace(n, m, N, endpoint=True)) # 从n 开始 到m结束 等距分成5个值,endpoint 是否包含结束点
print(np.concatenate((a,a**a))) # 多个数组合并
############################## ndarray 矩阵变换
a = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
print(a.shape)
print(a.reshape(4, 2)) # 改变数组，元素不变， 数组不变
print(a)
print(a.resize(11)) # 改变元数组，少的截取，多的0补充
# print(a.swapaxes(1, 3))
print(a.flatten()) # 进行数组的降维 原数组不变

###################### ndarray 类型转换
print(a.dtype)
b = a.astype(dtype=float)
print(b.dtype)
#################### ndarray 转list
print(a.tolist()) # 转化成python数组
print(type(a.tolist()))
print(type(a))
############索引 切片 一维数组
print(a)
print(a[1]) # 从0 开始
print(a[1:6:2]) # 开始 结束 步长
############索引 切片 二维数组
a = np.arange(24).reshape(2, 3, 4)
print(a)
print(a[0][1])# [] 表示多少维度，在这个维度里面的索引为几的元素
print(a[-1, 2, 3])
if 11 in a:
    print("aa")
print(a[-1, 2, 0:3:1])
print(a[:, -1, -1:])
print(a[:, :, -1:])
##############运算
a =  np.arange(4)
b = np.arange(4, 8)
print(a)
print(b)
print(a + b)
print(a - b)
print(a / b)
print(a * b)
a = np.arange(8).reshape((2, 4))
a = np.square(a)
print(a)
a = np.sqrt(a)
print(a)
print(np.fmax(a, b))
b = np.random.shuffle(a)
print(np.sqrt(a))

a = np.array([[0, 1, 2, 3, 4],
              [9, 8, 7, 6, 5]])
print(a.itemsize)
a = np.arange(10).reshape(2,5)
b = np.arange(10,20).reshape(2,5)
np.save("a.txt",a)
a = np.load("a.txt.npy")
print(a)
np.random.shuffle(a)
print(np.arange(12).reshape(3,4))
print(np.random.randint(100,200,(4,5)))
print(np.std(a))
print(np.arange(12).reshape(3,4,d))