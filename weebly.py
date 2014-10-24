#!/usr/local/Cellar python
import cgi, json, os, random, requests, urllib
from bson import json_util
from functools import wraps
from oauth2client.client import *
from bson import *
from flask import *
from flask.ext.pymongo import PyMongo

import settings
from settings import *

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)

app.debug = True
app.secret_key = secret_key

# TODO: 
# Stop the weird aggressive login
# Bind content deletions and make content updatable/editable
# Fix get all pages json
# Make active tab do ajax call to display the active page rather than default
# Add API Key requirement to RestAPI
# Better API return values and JSON success functions

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    print request.args
    token = 'api_token' in request.args and mongo.db.sessions.find_one({"weebly_token": request.args['api_token']})
    if not token and not session.get('user_id'):
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('index.html', pages=list(mongo.db.pages.find()), token=session['token'])

@app.route('/login')
def login():
    if session.get('user_id'):
      return redirect(url_for('index'))
    data = {}
    data['client_id'] = GOOGLE_APP_ID
    data['certificate'] = ''.join(random.choice("0123456789") for x in xrange(16))
    session['certificate'] = data['certificate']
    return render_template('login.html', data=data)

@app.route('/connect', methods=['POST'])
def connect():
  if request.args.get('certificate', '') != session['certificate']:
    return json.dumps({'error':'Invalid certificate.'})
  try:
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='', redirect_uri='postmessage')
    credentials = oauth_flow.step2_exchange(request.data)
  except FlowExchangeError:
    print "Flow Exchange Error"

  session['access_token'] = credentials.access_token
  session['user_id'] = credentials.id_token['sub']
  profile = json.load(urllib.urlopen("https://www.googleapis.com/plus/v1/people/me?" + 
                        urllib.urlencode({"access_token": credentials.access_token})))
  current_user = mongo.db.sessions.find_one({"user_id": credentials.id_token['sub'], "auth_type": "google"})
  if current_user:
    session['token'] = current_user["weebly_token"]
  else:
    session['token'] = "".join(random.sample(session['access_token'], 10))
    mongo.db.sessions.save({"access_token": session['access_token'], 
                           "user_id": session['user_id'],
                           "weebly_token": session['token'],
                           "info": profile,
                           "auth_type": "google"})
  return redirect(url_for('index'))

@app.route('/logout')
def logout():
  access_token = session.get('access_token')
  if access_token is None:
    return json.dumps({'error':'Current user not connected.'})
  if request.args.get('delete', ''): # deletes account & refreshes access_token on next sign in
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    urllib.urlopen(url)
    mongo.db.sessions.remove({"access_token": access_token})
  session.clear()
  return redirect(url_for('index'))

@app.route('/api/page/<page_id>', methods=['PUT'])
@requires_auth
def update_page(page_id):
  # db.pages.update({"name":"secod one", "elements":["teeheee"]}, { $set: {"elements.$" : "RUH ROH"} })
  print request.form
  if request.form.get('name'):
    mongo.db.pages.save({"_id": ObjectId(page_id), "name":request.form.get('name')})
  if request.form.get('elements'):
    mongo.db.pages.save({"_id": ObjectId(page_id), "elements":request.form.get('elements')})
  return json.dumps({"success":"updated!"})

@app.route('/api/page/<page_id>', methods=['DELETE'])
@requires_auth
def delete_page(page_id):
  if mongo.db.pages.remove(ObjectId(page_id)):
    return json.dumps({"deleted":page_id})

@app.route('/api/page/<page_id>', methods=['GET'])
@requires_auth
def get_page(page_id):
  print page_id
  return json.dumps(mongo.db.pages.find_one_or_404(ObjectId(page_id)), indent=4, default=json_util.default)

@app.route('/api/pages', methods=['GET'])
@requires_auth
def get_all_pages():
  for doc in mongo.db.pages.find():
    page_json = json.dumps(doc, indent=4, default=json_util.default)
  return page_json

@app.route('/api/pages', methods=['POST'])
@requires_auth
def new_page():
  name = request.form.get('name') or "Page"
  elements = request.form.get('elements') or DEFAULT_ELEMENTS
  new_id = mongo.db.pages.save({"name": name, "elements": elements})
  if new_id:
    return json.dumps({"success": str(new_id)})
  else:
    return json.dumps({"failure": "insertion failed"})

@app.route('/auth')
def auth():
    # Get access token 
    args = dict(client_id=FB_APP_ID, redirect_uri=FB_REDIRECT_URI, 
                code=request.args.get("code"), client_secret=FB_APP_SECRET)
    response_str = urllib.urlopen("https://graph.facebook.com/oauth/access_token?" 
                                    + urllib.urlencode(args)).read()
    # If token request fails, redirect back to login
    if response_str[0] == "{":
        del(args["client_secret"])
        return redirect("https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args))
    response = cgi.parse_qs(response_str)

    print "FACEBOOK OAUTH RESPONSE", response
    access_token = response["access_token"][-1]

    profile = json.load(urllib.urlopen("https://graph.facebook.com/me?" + 
                        urllib.urlencode({"access_token":access_token})))

    session['access_token'] = access_token
    session['user_id'] = profile['id']

    current_user = mongo.db.sessions.find_one({"user_id": profile['id'], "auth_type": "facebook"})
    if current_user:
      session['token'] = current_user["weebly_token"]
    else:
      session['token'] = "".join(random.sample(access_token, 10))
      mongo.db.sessions.save({"access_token": session['access_token'], # mongo save returns an ObjectID
                             "user_id": session['user_id'],
                             "weebly_token": session['token'],
                             "info": profile,
                             "auth_type": "facebook"})
    return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True, port=4000)
