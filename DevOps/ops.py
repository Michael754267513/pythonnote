# encoding: utf-8
from flask import Flask, render_template, request, redirect, make_response
from sql import db_sql
from users.users import user_dir,encrypt_md5
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_logs ={}
        role_list = {"SA": u"运维工程师", "Test": u"测试工程师"}
        username = str(request.form.get("username"))
        password = request.form.get("password")
        sql = "select role,name,password,id from users where name='%s'" % username
        user = db_sql.select_mysql(sql)
        for u1 in user:
            user_logs["role"] = role_list[u1[0]]
            user_logs["name"] = u1[1]
            user_logs["password"] = u1[2]
            user_logs["id"] = u1[3]
        if user and user_logs["password"] == encrypt_md5(password):
            resp = make_response(redirect("/index"))
            resp.set_cookie("username", user_logs["name"])
            resp.set_cookie("role", user_logs["role"])
            resp.set_cookie("id", str(user_logs["id"]))
            return resp
        else:
            return redirect("/")
        pass
    if request.method == "GET":
        return render_template("/")


@app.route("/index")
def root():
    user_cookies = request.cookies
    return render_template("index.html", **locals())


@app.route("/user/user_lists")
def user_lists():
    header_title, path1, path2, users, p = u'查看用户', u'用户管理', u'用户列表','',''
    sql = "select * from users"
    users = user_dir(db_sql.select_mysql(sql))
    user_cookies = request.cookies
    return render_template("user/user_lists.html", **locals())


@app.route("/user/user_add", methods=["POST", "GET"])
def user_add():
    header_title, path1, path2, users, p = u'', u'用户管理', u'添加用户', '', ''
    user_cookies = request.cookies
    if request.method == "GET":
        return render_template("/user/user_add.html", **locals())
    if request.method == "POST":
        sql = "select * from users where name = '%s' " % str(request.form["name"])
        if not db_sql.select_mysql(sql):
            sql = "INSERT INTO users(NAME,tel,mail,password,status,role) VALUES ('%s','%s','%s','%s','%s','%s')" % (str(request.form["name"]),
                                                                                          str(request.form["tel"]),
                                                                                          str(request.form["mail"]),
                                                                                          encrypt_md5(
                                                                                              str(request.form[
                                                                                                      "password"])),
                                                                                          str(request.form["status"]),
                                                                                          str(request.form["role"]))
            db_sql.update_mysql(sql)
    return redirect("/user/user_lists")


@app.route("/user/user_del", methods=["POST", "GET"])
def user_del():
    if request.method == "GET":
        Uid = request.args.get("id")
        sql = "DELETE FROM users WHERE  id = '%s'" % str(Uid)
        db_sql.update_mysql(sql)
        return "删除成功"
    if request.method == "POST":
        Uid = request.form["id"].split(",")
        for uid in Uid:
            sql = "DELETE FROM users WHERE  id = '%s'" % str(uid)
            db_sql.update_mysql(sql)
        return "删除成功"


@app.route("/user/user_edit", methods=["POST", "GET"])
def user_edit():
    if request.method == "GET":
        header_title, path1, path2, users, p = u'编辑用户', u'用户管理', u'编辑用户', '', ''
        if request.method == "GET":
            Uid = request.args.get("id")
        sql = "select * from users WHERE id = '%s'" % Uid
        users = user_dir(db_sql.select_mysql(sql))
        for ulist in users:
            user = ulist
        user_cookies = request.cookies
        return render_template("user/user_edit.html", **locals())
    if request.method == "POST":
        mail = str(request.form["mail"])
        phone = str(request.form["tel"])
        name = str(request.form["name"])
        status = str(request.form["status"])
        sql = "update users set  status = '%s',tel = '%s',mail = '%s' where name = '%s'" % (status, phone, mail, name)
        db_sql.update_mysql(sql)
        return  redirect("/user/user_lists")


@app.route("/user/user_lock", methods=["POST", "GET"])
def user_lock():
    if request.method == "GET":
        Uid = request.args.get("id")
        sql = "update users set  status = '0' where id = '%s'" % str(Uid)
        print sql
        db_sql.update_mysql(sql)
        return "锁定成功"
    return "锁定失败"


@app.route("/user/user_search")
def user_search():
    keyword = request.args.get("keyword")
    header_title, path1, path2, users, p = u'查看用户', u'用户管理', u'用户列表', '', ''
    sql = "select * from users WHERE name like '%" + "%s" % str(keyword) + "%'"
    users = user_dir(db_sql.select_mysql(sql))
    user_cookies = request.cookies
    return render_template("user/user_lists.html", **locals())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)