#encoding: utf-8
from flask import Flask, url_for, request
app   = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World  !"
#if __name__ == '__main__':
    #开启调试模式两种方式
    #app.debug = True
 #   app.run(host="0.0.0.0", port=80, debug=True)

@app.route("/name/<name>")
def hello_name(name):
    return "Hello %s" % name


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        return "POST"
    else:
        return "GET"


#测试请求
with app.test_request_context():
    #assert  request.path == "/login"
    #assert  request.method == "POST"
    print url_for("static", filename='index.html')
    print url_for("login")
    print url_for("hello_world")
    print url_for("hello_name", name="Michael")

