import numpy as np
import math


def computeR(X, Y): # 计算R 的方式一
    xBar = np.mean(X)# 求的是x的平均值 xbar
    #xBar = np.sum(X) / len(X)
    yBar = np.mean(Y)
    SSR = 0
    varX = 0
    varY = 0
    # SSR SST并非公式中提及到的SSR 和SST 而是R平方中提到的二次开方
    for i in  range(0, len(X)):
        X_Xbar = X[i] - xBar
        Y_Ybar = Y[i] - yBar
        SSR += X_Xbar * Y_Ybar
        varX += X_Xbar ** 2
        varY += Y_Ybar ** 2
    SST = math.sqrt(varX * varY)
    r = SSR / SST
    return r

testX = [1, 3, 8, 7, 9]
testY = [10, 12, 24, 21, 34]
print("R:" + str(computeR(testX, testY)))
print("R平方:" + str(computeR(testX, testY) ** 2))


# 第二种计算R平方 degress 表示X的平方数
def polyfit(X, Y, degree):
    coeffs = np.polyfit(X, Y, degree)
    # 计算y的期望值
    yhat = np.poly1d(coeffs)(X)
    # 计算y的平均值
    ybar = np.mean(Y)
    # SST = SSR + SSE
    SSR = np.sum((yhat - ybar) ** 2)
    SST = np.sum((Y - ybar) ** 2)
    SSE = np.sum((Y - yhat) ** 2)
    rSquare = SSR / SST
    return  rSquare

print("R平方：" + str(polyfit(testX, testY, 1)))