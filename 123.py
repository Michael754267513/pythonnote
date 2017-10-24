# # 1
# print(1 + 2)
# # 2
# L = [2,3,5,1]
# L.sort()
# print(L)
# # 3
# a = 'sdae'
# print(a[::-1])
# # 4
# a={1:1,2:2,3:3}
# print (",".join(map(str, sorted(a.keys()))))
# # 5
# a = 'asdasd'
# print(a[0:len(a):2])
#
L=[0,1,2,3,4,4,2,5,3,3,3]
L.sort()
if len(L)%2 == 0:
    print((L[int((len(L)/2))] + L[int((len(L)/2) - 1)])/2.0)
else:
    print(L[int((len(L)/2))])