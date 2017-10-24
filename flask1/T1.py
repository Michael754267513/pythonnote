# encoding: utf-8
from flask import Flask, render_template, request, redirect, make_response
from sql import db_sql
import json
from users.users import user_dir,encrypt_md5

app = Flask("__name__")


@app.route("/users")
def users():
    #sql = "select name,tel,mail from users"
    sql = "select * from users"
    data = db_sql.select_mysql(sql)
    username = ''
    role = ''
    if request.cookies:
        if  "username" in request.cookies:
            username = request.cookies["username"]
            role = request.cookies["role"]
    #print user_dir(data)
    return render_template("index.html", data=user_dir(data), username=username, role=role)


@app.route("/add_users", methods=["POST"])
def add_users():

    if not request.form.get("username"):
        return  redirect("/users")
    sql = "INSERT INTO users(NAME,tel,mail,password) VALUES ('%s','%s','%s','%s')" % (str(request.form["username"]),
                                                        str(request.form["tel"]),
                                                        str(request.form["mail"]),
                                                        encrypt_md5(
                                                              str(request.form["password"])))
    db_sql.update_mysql(sql)
    return redirect("/users")


@app.route("/select_user", methods=["POST"])
def select_user():
    user = request.form.get("username")
    sql = "select * from users where name like '%s'" % user
    data = db_sql.select_mysql(sql)
    return render_template("users.html", data=user_dir(data))


@app.route("/update_user",methods=["POST","GET"])
def update_user():
    if request.method == "POST":
        user = request.form.get("username")
        if not user:
            return "非法用户"
        sql = "select name,tel,mail from users where name like '%s'" % user
        data = db_sql.select_mysql(sql)
        if not data:
            return "不存在此用户"
        else:
            print "aa"
            return render_template("update_user.html", data=data)
    if request.method == "GET":
        user = request.args.get("username")
        tel  = request.args.get("tel")
        mail = request.args.get("mail")
        if not user and not tel and not mail:
            return "小伙淡定,慢慢慢来"
        sql = "UPDATE users SET tel='%s',mail='%s' WHERE users.`name`='%s'" % (tel, mail, user)
        db_sql.update_mysql(sql)
        return redirect("/users")


@app.route("/del_user",methods=["POST"])
def del_user():
    user = request.form.get("username")
    sql = "DELETE FROM users WHERE users.`name` = '%s' " % user
    db_sql.update_mysql(sql)
    return redirect("/users")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = str(request.form.get("username"))
        password = request.form.get("password")
        sql = "select role,password from users where name='%s'" % username
        user = db_sql.select_mysql(sql)
        print user[0][0]
        if user and user[0][1] == encrypt_md5(password):
            resp = make_response(redirect("/users"))
            resp.set_cookie("username", username)
            resp.set_cookie("role", user[0][0])
            return "success"
        else:
            return redirect("/login")
        pass
    if request.method == "GET":
        return render_template("login.html")

@app.route("/t1")
def test():
    p1 = {"name": "michael", "age": 22}
    return  render_template("t1.html", **locals())


@app.route("/ajax/btn02", methods=["POST", "GET"])
def ajax_btn02():
    if request.method == "GET":
        ulist = ["michael", "lao"]
        name = str(request.args.get("name"))
        if name in ulist:
            return "aaaaa"
        else:
            return name
    if request.method == "POST":
        name = request.form["name"]
        return "你好 %s" % str(name)

@app.route("/michael")
def michael():
    return render_template("michael.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)