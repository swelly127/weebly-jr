#!/usr/local/Cellar python
import cgi, datetime, json, os, random, requests, urllib
import settings

from bson import *
from bson import json_util

from oauth2client.client import *
from settings import *
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)


app.debug = True
app.secret_key = secret_key

@app.route('/')
def index():
    print session
    data = {}
    if 'gplus_id' not in session:
      data['client_id'] = GOOGLE_APP_ID
      data['redirect_uri'] = REDIRECT_URI
      data['certificate'] = ''.join(random.choice("0123456789") for x in xrange(16))
      session['certificate'] = data['certificate']
      return render_template('logged_out.html', data=data)
    return render_template('logged_in.html', pages=list(mongo.db.pages.find()))

@app.route('/connect', methods=['POST'])
def connect():
  """Exchange the one-time authorization code for a token and
  store the token in the session."""

  print request, session['certificate']
  # Ensure that the request isn't a forgery
  if request.args.get('certificate', '') != session['certificate']:
    return json.dumps({'error':'Invalid certificate.'})

  try:
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='', redirect_uri='postmessage')
    credentials = oauth_flow.step2_exchange(request.data)
  except FlowExchangeError:
    print "flow exchange error"

  session['access_token'] = credentials.access_token
  session['gplus_id'] = credentials.id_token['sub']
  print session
  return render_template('logged_in.html', pages=mongo.db.pages.find())

@app.route('/disconnect')
def disconnect():
  # Only disconnect a connected user.
  access_token = session.get('access_token')
  if access_token is None:
    return json.dumps({'error':'Current user not connected.'})

  # Execute HTTP GET request to revoke current token.
  url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
  urllib.urlopen(url)

  session.clear()
  return redirect(url_for('index'))

@app.route('/login')
def login():
    args = dict(client_id=FACEBOOK_APP_ID, redirect_uri="http://localhost:5000/auth")
    return redirect("https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args))

@app.route('/auth')
def auth():
    """ Extract authorization token """
    args = dict(client_id=FACEBOOK_APP_ID, redirect_uri="http://localhost:5000/auth")
    args["client_secret"] = FACEBOOK_APP_SECRET  
    args["code"] = request.args.get("code")


    """ Get access token """
    response_str = urllib.urlopen(
        "https://graph.facebook.com/oauth/access_token?" +
        urllib.urlencode(args)).read()

    """ If token request fails, redirect back to login """
    if response_str[0] == "{":
        del(args["client_secret"])
        return redirect(
        "https://graph.facebook.com/oauth/authorize?" +
        urllib.urlencode(args))
    response = cgi.parse_qs(response_str)
    access_token = response["access_token"][-1]


    """ Get profile data """
    profile = json.load(urllib.urlopen(
        "https://graph.facebook.com/me?" +
        urllib.urlencode(dict(access_token=access_token))))
    user_id = profile['id']
    session['access_token'] = access_token
    session['user_id'] = user_id

    user = Users.query.filter_by(id=user_id).first()

    if user is None:
        user = Users(user_id)

    user.access_token = access_token
    user.name = profile['first_name'] + profile['last_name']

    mongo.db.session.add(user)
    mongo.db.session.commit()

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/page/<page_id>', methods=['PUT'])
def update_page(page_id):
    if not session.get('gplus_id'):
        return render_template('logged_out.html')
    print request.form
    if request.form.get('name'):
      mongo.db.pages.save({"_id": ObjectId(page_id), "name":request.form.get('name')})
    if request.form.get('elements'):
      mongo.db.pages.save({"_id": ObjectId(page_id), "elements":request.form.get('elements')})
    return json.dumps({"success":"updated!"})

@app.route('/api/page/<page_id>', methods=['DELETE'])
def delete_page(page_id):
    if not session.get('gplus_id'):
        return render_template('logged_out.html')
    if mongo.db.pages.remove(ObjectId(page_id)):
      return json.dumps({"deleted":page_id})

@app.route('/api/page/<page_id>', methods=['GET'])
def get_page(page_id):
    if not session.get('gplus_id'):
        return render_template('logged_out.html')
    print page_id
    return json.dumps(mongo.db.pages.find_one_or_404(ObjectId(page_id)), default=json_util.default)

@app.route('/api/pages', methods=['GET'])
def get_all_pages():
    if not session.get('gplus_id'):
        return render_template('logged_out.html')
    for doc in mongo.db.pages.find():
      page_json = json.dumps(doc, sort_keys=True, indent=4, default=json_util.default)
    return page_json

@app.route('/api/pages', methods=['POST'])
def new_page():
  if not session.get('gplus_id'):
    return render_template('logged_out.html')
  name = request.form.get('name') or "Page"
  elements = request.form.get('elements') or DEFAULT_ELEMENTS
  new_id = mongo.db.pages.save({"name": name, "elements": elements})
  if new_id:
    return json.dumps({"success": str(new_id)})

if __name__ == "__main__":
	app.run(debug=True, port=4000)
