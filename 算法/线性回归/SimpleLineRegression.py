import numpy as np

print('方程：y = b0 + b1*x')


def fitSLR(x, y):
    n = len(x)
    numerator = 0
    denominator = 0
    for i in range(0, n):
        numerator += (x[i] - np.mean(x)) * (y[i] - np.mean(y))
        denominator += (x[i] - np.mean(x))**2
        b1 = numerator/float(denominator)
        b0 = float(np.mean(y)) - b1 * np.mean(x)
    print("斜率等于：%f" % b1)
    print("Y的截距：%f" % b0)
    print("方程式：y = %f + %f*x" %(b0, b1))
    return b0, b1

def predict(x, b0, b1):
    return b0 + x * b1

# 自变量x为广告投放量，因变量y为销售数量
x = [1, 3, 2, 1, 3]
y = [14, 24, 18, 17, 27]

b0 , b1 = fitSLR(x, y)

x_input = 2
y_output = predict(x_input, b0, b1)
print("预测值：%f" % y_output)
