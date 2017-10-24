#!encoding: utf-8
from sklearn.feature_extraction import DictVectorizer
import csv
from sklearn import tree
from sklearn import preprocessing
from sklearn.externals.six import StringIO

# 读取信息样本
allElectronicsData = open(r'itwork.csv', 'rt')
reader = csv.reader(allElectronicsData)

# 获取标题头部信息
for row in reader:
    headers = row
    break

print(headers)

# 属性列表
attList = []
# 结果列表
labelList = []

# 数据组装
for row in reader:
    labelList.append(row[len(row)-1])  # 获取结果列表
    rowDict = {}
    for i in range(0, len(row)-1):
        rowDict[headers[i]] = row[i]  # 样本属性组装
    attList.append(rowDict)
#
print(attList)
print (labelList)

# 向量化属性样本
vec = DictVectorizer()
dummyX = vec.fit_transform(attList) .toarray()  # 转换成 0 1

# 转换对应标准
print(vec.get_feature_names())
# 转换后的列表
print("dummyX: " + str(dummyX))
# 结果列表
print("labelList: " + str(labelList))

# 向量化结果
lb = preprocessing.LabelBinarizer()
dummyY = lb.fit_transform(labelList)
print("dummyY: " + str(dummyY))
# Using decision tree for classification
# clf = tree.DecisionTreeClassifier()
clf = tree.DecisionTreeClassifier(criterion='entropy')  # 采用Dtree 的 熵
clf = clf.fit(dummyX, dummyY)
print("clf: " + str(clf))

# Visualize model
with open("ITwork.dot", 'w', encoding='utf-8') as f:
    f = tree.export_graphviz(clf, feature_names=vec.get_feature_names(), out_file=f)

oneRowX = dummyX[0, :]
print("oneRowX: " + str(oneRowX))

newRowX = oneRowX
newRowX[0] = 1
newRowX[2] = 0
print("newRowX: " + str(newRowX))

predictedY = clf.predict(newRowX.reshape(1, -1))
print("predictedY: " + str(predictedY))
