from numpy import genfromtxt
from sklearn import linear_model


datafile = r"Delivery.csv"
# delimiter 分隔符号
dataDelivery = genfromtxt(datafile, delimiter=",")
print("数据集：")
print(dataDelivery)
X = dataDelivery[:, :-1]
Y = dataDelivery[:, -1]
print("X 自变量数据集：")
print(X)
print("Y 因变量数据集：")
print(Y)

regr = linear_model.LinearRegression()
regr.fit(X, Y)
print("斜率：b1 b2")
print(regr.coef_)
print("截距: b0")
print(regr.intercept_)

xPred =[[102, 6]]
yPred = regr.predict(xPred)
print("预测值(因变量)：")
print(yPred)