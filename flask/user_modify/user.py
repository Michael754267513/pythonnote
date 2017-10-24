import pickle
import user_modify

def load_file():
    loadfile = open("../users", "rb")
    user_list = pickle.load(loadfile)
    loadfile.close()
    return user_list

def dump_file(username, password):
    users_list = "%s:%s" % (username, password)
    f1 = open("../users", "ab")
    pickle.dump(users_list, f1)
    f1.close()
#dump_file("user1", "pwd1")