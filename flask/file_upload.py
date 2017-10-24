from flask import  Flask, request
app = Flask(__name__)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["a.txt"]
        f.save('b.txt')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
