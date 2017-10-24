import cPickle as pickle

a = [1, 2, 3]
b = a
dd = a.append(a)
print dd
print a
print b
a.append(4)
print a
print b
c = pickle.dumps(a)
print c
cc = pickle.loads(c)
print cc
