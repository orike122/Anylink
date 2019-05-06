from flask import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

def start_website():
    app.run("127.0.0.1",8888)

def get_database():
    # TODO return implentation
    pass
def get_requests_manager():
    # TODO return implentation
    pass
if __name__ == "__main__":
    start_website()