# encoding: utf-8
import hashlib


def user_dir(data):
    dir_users = {}
    list_user = []
    for user in data:
        dir_users[u"用户名"] = user[1]
        dir_users[u"电话号码"] = user[2]
        dir_users[u"邮箱地址"] = user[3]
        dir_users[u"角色"] = user[4]
        dir_users[u"用户状态"] = user[5]
        list_user.append(dir_users)
        dir_users = {}

    return list_user


def encrypt_md5(password):
    md = hashlib.md5()
    md.update(password)
    md5 = md.hexdigest()
    return md5