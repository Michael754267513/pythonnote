# encoding: utf-8
import hashlib


def user_dir(data):
    dir_users = {}
    list_user = []
    for user in data:
        dir_users[u"id"] = user[0]
        dir_users[u"name"] = user[1]
        dir_users[u"phone"] = user[2]
        dir_users[u"mail"] = user[3]
        dir_users[u"role"] = user[4]
        dir_users[u"password"] = user[6]
        if user[5] == 0:
            dir_users[u"status"] = u"可用"
        else:
            dir_users[u"status"] = u"锁定"
        list_user.append(dir_users)
        dir_users = {}

    return list_user


def encrypt_md5(password):
    md = hashlib.md5()
    md.update(password)
    md5 = md.hexdigest()
    return md5