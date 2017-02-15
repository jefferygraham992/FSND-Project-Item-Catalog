from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CharacterType, Character, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///thomascatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIS
@app.route('/catalog/JSON')
def catalogJSON():
    inventory = session.query(CharacterType).all()
    return jsonify(inventory=[train_kind.serialize for train_kind in inventory])


@app.route('/catalog/<train_type>/JSON')
def trainsJSON(train_type):
    trains = session.query(Character).filter_by(character_kind=train_type).all()
    return jsonify(engines=[train.serialize for train in trains])


@app.route('/catalog/<train_type>/<train_name>/JSON')
def trainJSON(train_type, train_name):
    train = session.query(Character).filter_by(character_name=train_name).one()
    return jsonify(train=train.serialize)


# show all train categories & latest trains
@app.route('/')
@app.route('/catalog')
def showCatalog():
    inventory = session.query(CharacterType).order_by(asc(CharacterType.id))
    latest_trains = session.query(Character).limit(10)
    if 'username' not in login_session:
        return render_template('publicshowcatalog.html', inventory=inventory, latest_trains=latest_trains)
    else:
        return render_template('showcatalog.html', inventory=inventory, latest_trains=latest_trains)


# show all trains in one category
@app.route('/catalog/<train_type>')
@app.route('/catalog/<train_type>/trains')
def showTrains(train_type):
    inventory = session.query(CharacterType).all()
    trainType = session.query(CharacterType).filter_by(type_name=train_type).one()
    trains = session.query(Character).filter_by(character_kind=train_type).all()
    if 'username' not in login_session:
        return render_template('publicshowtrains.html', trainType=trainType, trains=trains, inventory=inventory)
    else:
        return render_template('showtrains.html', trainType=trainType, trains=trains, inventory=inventory)


# show info for one train
@app.route('/catalog/<train_type>/<train_name>')
def showTrain(train_type, train_name):
    train = session.query(Character).filter_by(character_name=train_name).one()
    creator = getUserInfo(train.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicshowtrain.html', train=train, creator=creator)
    else:
        return render_template('showtrain.html', train=train, creator=creator)


# add a train
@app.route('/catalog/add', methods=['GET', 'POST'])
def addTrain():
    if 'username' not in login_session:
        return redirect('/login')
    inventory = session.query(CharacterType).all()
    if request.method == 'POST':
        newTrain = Character(character_name=request.form['character_name'], description=request.form['description'], character_kind=request.form['character_kind'], character_picture=request.form['character_picture'], user_id=login_session['user_id'])
        session.add(newTrain)
        flash('%s successfully added!' % newTrain.character_name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newtrain.html', inventory=inventory)


# edit a train
@app.route('/catalog/<train_name>/edit', methods=['GET', 'POST'])
def editTrain(train_name):
    if 'username' not in login_session:
        return redirect('/login')
    inventory = session.query(CharacterType).all()
    editedTrain = session.query(Character).filter_by(character_name=train_name).one()
    if editedTrain.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this train. Please create your own train in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['character_name']:
            editedTrain.character_name = request.form['character_name']
        if request.form['description']:
            editedTrain.description = request.form['description']
        if request.form['character_kind']:
            editedTrain.character_kind = request.form['character_kind']
        if request.form['character_picture']:
            editedTrain.character_picture = request.form['character_picture']
        session.add(editedTrain)
        flash('%s edited successfully!' % editedTrain.character_name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('edittrain.html', editedTrain=editedTrain, inventory=inventory)


# delete a train
@app.route('/catalog/<train_name>/delete', methods=['GET', 'POST'])
def deleteTrain(train_name):
    if 'username' not in login_session:
        return redirect('/login')
    trainToDelete = session.query(Character).filter_by(character_name=train_name).one()
    if trainToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this train. Please create your own train in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(trainToDelete)
        flash('%s successfuly deleted!' % trainToDelete.character_name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deletetrain.html', trainToDelete=trainToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
