# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, make_response
app = Flask(__name__)


@app.route("/hello")
@app.route("/hello/<name>")
def hello(name="ZengHao"):
    print request.cookies["username"]
    return render_template("hello.html", name=name)


@app.route("/Welcome")
def welcome():
    return render_template("Welcome.html", username=request.cookies["username"])


@app.route("/check_users")
def check_users():
    users = {"michael": "123456", "laoshu": "654321"}
    username = str(request.args.get("username", ""))
    password = str(request.args.get("password", ""))
    if username in users.keys():
        if password == users[username]:
            resp = make_response(redirect("/Welcome"))
            resp.set_cookie("username", username)
            return resp
        else:
            return render_template("message_user.html")
    else:
        return redirect("/login")


@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)