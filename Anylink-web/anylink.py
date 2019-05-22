from flask import *
from flask_sslify import SSLify
from functools import wraps
from utils import PathBuilder
import hashlib
from threading import Lock
import os
import logging


app = Flask(__name__,static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

sslify = SSLify(app,permanent=True)

request_manager = None
account_manager = None
current_paths = {}
file_transfer_mutex = Lock()
def get_file_transfer_mutex():
    global file_transfer_mutex
    return file_transfer_mutex

def hold_until_transfered():
    transfered =False
    logging.info("Waiting for file to be transfered")
    while not transfered:
        email_hash = hashlib.sha256(session['user'].encode("utf-8")).hexdigest()
        fpath = "/{email_hash}/storage".format(email_hash=email_hash)
        transfered = os.path.exists(PathBuilder(fpath) + session['file_to_download'])
    logging.info("File successfully transfered")


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

@app.route("/",methods=['GET'])
@login_required
def home():
    get_requests_manager().accept_user_clients(session['user'])
    chans = get_requests_manager().get_user_channels(session['user'])
    return render_template("home.html",chans=chans)

@app.route("/file_browser")
@login_required
def file_browser():
    chans = get_requests_manager().get_user_channels(session['user'])
    req = request.args.get('jsdata')
    tp,name = req.split(',')
    logging.info("File browser got request for {type}: {name}".format(type=tp,name=name))
    if tp == 'back':
        session['current_path'] = PathBuilder(session['current_path']) - 1
    elif tp == 'dir':
        session['current_path'] = PathBuilder(session['current_path']) + name
    elif tp == 'file':
        get_requests_manager().send_file(chans[0],PathBuilder(session['current_path']) + name)
        session['file_to_download'] = name
        logging.info("Downloading file: {name}".format(name = session['file_to_download']))
        hold_until_transfered()
        get_requests_manager().accept_user_clients(session['user'])
        chans = get_requests_manager().get_user_channels(session['user'])

    logging.info("Got file tree request for: {path}".format(path=session['current_path']))
    dirs, files = get_requests_manager().send_tree(chans[0], session['current_path'])
    dirs = [d.decode('utf-8') for d in dirs]
    files = [f.decode('utf-8') for f in files]
    logging.info("Successfully obtain file tree")
    return render_template("file_browser.html",dirs = dirs,files=files)
@app.route("/download_file")
@login_required
def download_file():
    if 'file_to_download' in session and session['file_to_download'] is not None:
        logging.info("Found download file")
        f = session['file_to_download']
        session['file_to_download'] = None
        email_hash = hashlib.sha256(session['user'].encode("utf-8")).hexdigest()
        fpath = "/{email_hash}/storage".format(email_hash=email_hash)
        return send_from_directory(fpath,f,as_attachment=True)

@app.route("/login",methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if validate_login(request.form['username'],
                          request.form['password']):
            session['user'] = request.form['username']
            session['current_path'] = '/'
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
