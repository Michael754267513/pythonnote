from flask import render_template, Flask, request
app = Flask(__name__)


@app.route("/hello")
@app.route("/hello/<name>")
def hello(name):
    #return  "Hello %s" % name
    return render_template("index.html", name=name)
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
       return "qazwsx"
    else:
        #get uri args
        searchkeys = request.args.get("username", "password")
        return "%s" % searchkeys
@app.route("/users")
def users():
    username = request.args.get("username")
    password = request.args.get("password")
    return  "username: %s \n password: %s" % (username, password)
@app.route("/list_users")
def list_users():
    users = open("users", "r").readlines()
    print users
    return render_template("list_users.html", users = users)
@app.route("/add_users", methods=["POST"])
def add_users():
    username = request.form("username")
    password = request.form("password")
    return "%s:%s" % (username, password)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
