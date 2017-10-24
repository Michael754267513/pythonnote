# encoding: utf-8
from flask import Flask, render_template, request, redirect
import user_modify.user_modify
app = Flask(__name__)


@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))
    if user_modify.user_modify.select_user(username) == False:
        user_modify.user_modify.user_add(username, password)
        return redirect("/users")
    else:
        return "%s用户已存在" % username

@app.route("/select_user", methods=["POST", "GET"])
def select_user():
        username = str(request.args.get("username"))
        users_list = user_modify.user_modify.select_user(username)
        users_list = [users_list]
        return render_template("user_list1.html", users=users_list)

@app.route("/users")
def list_users():
    users_list = user_modify.user_modify.select_users()
    return render_template("user_list1.html", users = users_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)