from flask import *
from flask_sslify import SSLify
from functools import wraps

app = Flask(__name__,static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

sslify = SSLify(app,permanent=True)

request_manager = None
account_manager = None

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def home():
    get_requests_manager().accept_user_clients(session['user'])
    chans = get_requests_manager().get_user_channels(session['user'])
    return render_template("home.html",chans=chans)

@app.route("/login",methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if validate_login(request.form['username'],
                          request.form['password']):
            session['user'] = request.form['username']
            return redirect(url_for('home'))
        else:
            error = 'login failed!'
    return render_template('login.html',error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop('user',None)
    return redirect(url_for('logout'))

def validate_login(username,password):
    return get_account_manager().validate_user(username,password)


def start_website(r_manager,a_manager):
    global request_manager,account_manager
    request_manager = r_manager
    account_manager = a_manager
    app.run("0.0.0.0",443,debug=False,ssl_context=('anylinknow.pem','private.pem'))

def get_account_manager():
    global account_manager
    return account_manager
def get_requests_manager():
    global request_manager
    return request_manager