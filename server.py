import json
from pickle import TRUE
import profile
from flask import Flask, render_template, request, g, redirect, url_for, jsonify, send_file, session
from werkzeug.utils import secure_filename
import io
import time
import db
from os import environ as env
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from dotenv import load_dotenv, find_dotenv
from werkzeug.exceptions import HTTPException
from functools import wraps
import json

import sys
import db

app = Flask(__name__)
app.secret_key = env.get('SECRET_KEY')
oauth = OAuth(app)

auth0_domain = env.get('AUTH0_DOMAIN')
auth0_client_id = env.get('AUTH0_CLIENT_ID')
auth0_client_secret = env.get('AUTH0_CLIENT_SECRET')

def fetch_token(name, request):
    token = OAuth2Token.find(
        name=name,
        user=request.user
    )
    return token.to_token()

auth0 = oauth.register(
    'auth0',
    client_id=auth0_client_id,
    client_secret=auth0_client_secret,
    api_base_url=f'https://{auth0_domain}',
    access_token_url=f'https://{auth0_domain}/oauth/token',
    authorize_url=f'https://{auth0_domain}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{auth0_domain}/.well-known/openid-configuration',
    # jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
    fetch_token=fetch_token,
    )

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect(url_for('login'))
    return f(*args, **kwargs)

  return decorated

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect(url_for('personal'))

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback_handling', _external=True))

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': auth0_client_id}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.before_first_request
def initialize():
    db.setup()


@app.route('/',methods=['POST','GET'])
def home():
    with db.get_db_cursor() as cur:
        audio_if = {}
        if request.method == 'POST':
            print('===========================================', file=sys.stderr)
            string = request.form['searchbox']
            audio_ids = db.public_search(string)
            print(f'audio_ids: {audio_ids}', file=sys.stderr)
        else:
            audio_ids = db.get_all_public_audio_ids()
        for aid in audio_ids:

            info_data = db.get_audio(aid)

            audio_if[aid] = {
                "person_id" : info_data['person_id'],
                "timecreate" : info_data['timecreate'],
                "filename" : info_data['filename'],
                "description" : info_data['description'],
                #"search" : info_data.search,
                "publicity" : info_data['publicity']
            }
        return render_template("main.html", audio_ids = audio_ids, audio_info = audio_if)



@app.route('/<int:audio_id>')
def view_audio(audio_id):
    audio_row = db.get_audio(audio_id)
    #print(audio_row, file=sys.stderr)
    stream = io.BytesIO(audio_row["data"])
         
    # use special "send_file" function
    return send_file(stream, attachment_filename="audio.mp3")

'''
@app.route('/description/<int:audio_id>')
def view_description(audio_id):
    audio_description = db.get_audio_description(audio_id)
    print("nshjabhxcjead", file=sys.stderr)
    print(f"audio description: {audio_description}", file=sys.stderr)
    return audio_description
'''


@app.route('/personal', methods=['POST','GET'])
@requires_auth
def personal():
    persnal_id = session['profile']['user_id']
    with db.get_db_cursor() as cur:
        audio_if = {}
        if request.method == 'POST':
            print('===========================================', file=sys.stderr)
            search = request.form['searchbox']
            audio_ids = db.private_search(persnal_id,search)
            print(f'audio_ids: {audio_ids}', file=sys.stderr)

        else:    
            audio_ids = db.get_audio_personal(persnal_id)
        for aid in audio_ids:
            info_data = db.get_audio(aid)
            audio_if[aid] = {
                "person_id" : info_data['person_id'],
                "timecreate" : info_data['timecreate'],
                "filename" : info_data['filename'],
                "description" : info_data['description'],
                #"search" : info_data.search,
                "publicity" : info_data['publicity']
            }    
        return render_template("personal.html", audio_ids = audio_ids, audio_info = audio_if)



# @app.route('/personal', methods=['GET'])
# def personal():
#     audio_ids =
#     return render_template('personal.html', audio_ids=audio_ids)




# @app.route('/searchingprivate',methods=['POST','GET'])
# def searchp():
#     if request.method == 'POST':
#         user = request.form['searchbox']
#         # return render_template('index.html',audio_ids = db.public_search(user))
#         # return jsonify(db.public_search(user))
#         return render_template("index_return.html", audio_ids=db.private_search(user))
#     else:
#         return render_template("index_return.html")


# @app.route('/audio', methods=['POST'])
# def upload_audio():
#     # check if the post request has the file part
#     if 'audio' not in request.files:
#         return redirect(url_for('/personal', status="Audio Upload Failed: No selected file"))
#     file = request.files['audio']
#     # if user does not select file, browser also
#     # submit an empty part without filename
#     if file.filename == '':
#         return redirect(url_for('/personal', status="Audio Upload Failed: No selected file"))
#     if file and allowed_audio_file(file.filename):
#         filename = secure_filename(file.filename)
#         data = file.read()
#         db.upload_audio(data, filename)
#     return redirect(url_for("personal", status="Audio Uploaded Succesfully"))

def allowed_audio_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['mp3', 'wav', "ogg"]



@app.route('/audio', methods=['POST'])
@requires_auth
def upload_audio():
    # check if the post request has the file part
    if 'audio' not in request.files:
        return redirect(url_for("personal", status="Audio Upload Failed: No selected file"))
    file = request.files['audio']
    if 'select_audio_description' in request.form:
        description = request.form['select_audio_description']
        if (request.form['publicity'] == 'true'):
            publicity = 0
        else:
            publicity = 1
    person_id = session['profile']['user_id']
    
    
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return redirect(url_for("personal", status="Audio Upload Failed: No selected file"))
    if file and allowed_audio_file(file.filename):
        filename = secure_filename(file.filename)
        data = file.read()

        db.upload_audio(description, data,person_id,publicity)

    return redirect(url_for("personal" , status="audio Uploaded Succesfully"))


# add personal ID
@app.route('/audio', methods=['GET'])
def audio_gallery():
    status = request.args.get("status", "")
    with db.get_db_cursor() as cur:
        audio_ids = db.get_audio_ids()
        return render_template("personal.html", audio_ids = audio_ids)
    
    
@app.route('/audio', methods=['GET'])
def audio_main_page_gallery():
    status = request.args.get("status", "")
    with db.get_db_cursor() as cur:
        audio_ids = db.get_audio_ids()
        return render_template("personal.html", audio_ids = audio_ids)



@app.route('/audio/<int:audio_id>', methods=['POST'])
def delete_audio(audio_id):

    db.delete_audio_ids(audio_id)
    return redirect(url_for("personal", status="audio Deleted Successfully"))

@app.route('/audio/<int:audio_id>', methods=['POST'])
def change_publicity_audio(audio_id,publicity):
    if publicity ==0:
        db.set_audio_pubclity(audio_id,1)
    else:
        db.set_audio_pubclity(audio_id,0)

    return redirect(url_for("personal", status="audio Deleted Successfully"))
