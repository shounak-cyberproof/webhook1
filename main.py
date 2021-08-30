from flask import Flask, request, abort
from run_process import run_process

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        run_process()
        return "success", 200
    else:
        abort(400)


if __name__=="__main__":
    app.run()