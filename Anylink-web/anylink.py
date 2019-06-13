from flask import *
from flask_sslify import SSLify
from functools import wraps
from utils import PathBuilder
import hashlib
import os
import logging
import types


app = Flask(__name__,static_url_path='/static') #Define static folder path
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #Define age file, in order to not save cached static files
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #Define secret key

sslify = SSLify(app,permanent=True) #SSLify the original app

get_account_manager: types.FunctionType
get_requests_manager: types.FunctionType
current_paths = {} #Current user paths

def hold_until_transfered():
    """Blocks until the file that is currently being transfered, finishes"""
    transfered =False
    logging.info("Waiting for file to be transfered")
    while not transfered:
        email_hash = hashlib.sha256(session['user'].encode("utf-8")).hexdigest()
        fpath = "/{email_hash}/storage".format(email_hash=email_hash)
        transfered = os.path.exists(PathBuilder(fpath) + session['file_to_download'])
    logging.info("File successfully transfered")


@app.before_request
def before_request():
    """Converts http request to a secured HTTP connection"""
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

def login_required(f):
    """Wrapper function that requires login for views"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/",methods=['GET'])
@login_required
def home():
    """View that respones with the home page"""
    return render_template("home.html")

@app.route("/get_clients",methods=['GET'])
@login_required
def get_clients():
    """View that responses with the clients list"""
    get_requests_manager().accept_user_clients(session['user'])
    chans = get_requests_manager().get_user_channels(session['user'])
    return render_template("client_list.html", chans=chans)

@app.route("/settings",methods=['GET','POST'])
@login_required
def settings():
    """View that responses with the settings page"""
    if request.method == "POST":
        key = request.form['key']
        email_hash = hashlib.sha256(session['user'].encode("utf-8")).hexdigest()
        filename = "/{email_hash}/ssh/authorized_keys".format(email_hash=email_hash)
        with open(filename,"a") as f:
            f.write(key+"\n")
    return render_template("settings.html")

def get_chan_by_id(chans,id):
    """Searches channel from a list of channels by id"""
    chan = [c for c in chans if c.get_name()==id]
    for c in chan:
        logging.debug("id: {id}".format(id=c.get_name()))
    print("................................"+str(len(chan)))
    if len(chan) == 1:
        return chan[0]
    return None

@app.route("/file_browser")
@login_required
def file_browser():
    """View that responses with the file browser page"""
    chans = get_requests_manager().get_user_channels(session['user'])
    req = request.args.get('jsdata')
    tp,name,id = req.split(',')
    id = id
    chan = get_chan_by_id(chans,id)
    if 'current_client' not in session or session['current_client'] is None:
        session['current_client'] = id
        name = '/'
        tp = 'dir'
    elif session['current_client'] != id:
        session['current_client'] = id
        name = '/'
        tp = 'dir'
    else:
        if tp == 'back':
            session['current_path'] = PathBuilder(session['current_path']) - 1
        elif tp == 'dir':
            session['current_path'] = PathBuilder(session['current_path']) + name
        elif tp == 'file':
            res = get_requests_manager().send_file(chan,PathBuilder(session['current_path']) + name)
            if not res:
                return abort(404)

            session['file_to_download'] = name
            logging.info("Downloading file: {name}".format(name = session['file_to_download']))


    logging.info("File browser got request for {type}: {name} at {id}".format(type=tp, name=name, id=id))
    logging.info("Got file tree request for: {path}".format(path=session['current_path']))
    logging.info("Current chan: {chan}".format(chan=chan))
    dirs, files = get_requests_manager().send_tree(chan, session['current_path'])
    dirs = [d.decode('utf-8') for d in dirs]
    files = [f.decode('utf-8') for f in files]
    logging.info("Successfully obtain file tree")
    return render_template("file_browser.html",dirs = dirs,files=files)
@app.route("/download_file")
@login_required
def download_file():
    """View that responses with the downloaded file"""
    if 'file_to_download' in session and session['file_to_download'] is not None:
        logging.info("Found download file")
        f = session['file_to_download']
        session['file_to_download'] = None
        email_hash = hashlib.sha256(session['user'].encode("utf-8")).hexdigest()
        fpath = "/{email_hash}/storage".format(email_hash=email_hash)
        return send_from_directory(fpath,f,as_attachment=True)

@app.route("/login",methods=['POST','GET'])
def login():
    """View that responses with the login page"""
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

@app.route("/validate_user",methods=['POST'])
def validate_user():
    """View that responses with a validation answer"""
    json = {'valid':False}
    logging.debug("Validation request: {req}".format(req=request.json))
    if validate_login(request.json['email'],
                      request.json['passh']):
        json['valid'] = True
    return jsonify(json)

@app.route("/signup",methods=['POST','GET'])
def signup():
    """View that responses with the sign up page"""
    error = None
    if request.method == 'POST':
        if create_user(request.form['username'],
                       request.form['password']):
            return redirect(url_for('login'))
        else:
            error = 'registration failed: email already exists'
    return render_template('signup.html',error=error)

@app.route("/logout")
@login_required
def logout():
    """View that responses with the log out page"""
    session.pop('user',None)
    return redirect(url_for('logout'))

def validate_login(username: str,password: str) -> bool:
    """
    Util function for user validation against DB
    :param username: User's email
    :param password: User's password hash
    :return: Is user valid
    """
    return get_account_manager().validate_user(username,password)

def create_user(email: str,passwordh: str) -> bool:
    """
    Util function for user validation against DB
    :param email:  User's email
    :param passwordh: User's password hash
    :return: Is user created

    """
    return get_account_manager().create_user(email,passwordh)

def start_website():
    """Starts flask web server"""
    app.run("0.0.0.0",443,debug=False,ssl_context=('anylinknow.pem','private.pem'))

