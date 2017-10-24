# encoding: utf-8
def open_user_list(mode):
    file = open("G:\\code\\flask\\users", mode)
    return file

#增加用户
def user_add(username, password):
    data = "\n%s:%s" % (username, password)
    open_user_list("a").write(data)

#删除用户
def del_user(username):
    pass

#查询用户
def select_user(username):
   for user in open_user_list("r"):
      if username == user.split(":")[0]:
          return user.split(":")
   return False

def select_users():
    us =[ line.split(":")  for line in open_user_list("r").read().split("\n") ]
    return  us
#修改用户
def modify_user(user_att):
    pass

