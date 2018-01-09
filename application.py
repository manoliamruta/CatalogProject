""" Necessary Imports """
import random
import string
import httplib2
import json
import requests
import datetime

from flask import Flask, render_template, url_for, \
    request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item, User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catalog/<int:category_id>/JSON')
def categoryItemJSON(category_id):
    """ This function is the JSON endpoint for displaying
    the particular category in the catalog whose id is specified. """
    category = session.query(Category).\
        filter_by(id=category_id).one()
    items = session.query(Item).\
        filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    """ This function is the JSON endpoint for displaying
    the particular item in the category whose ids
    are specified. """
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


@app.route('/catalog/JSON')
def categoriesJSON():
    """ This function is the JSON endpoint for displaying
    all the categories. """
    categories = session.query(Category).all()
    return jsonify(Categories=[r.serialize for r in categories])


@app.route('/')
@app.route('/catalog/')
def showallCategories():
    """ This function shows all the Categories present
    in the Catalog. """
    category = session.query(Category).all()
    onedayearly = datetime.timedelta(hours=24)
    since = datetime.datetime.now() - onedayearly
    latest = session.query(Item).filter(Item.date > since)
    return render_template('category.html', category=category, latest=latest)


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/item/')
def showCategory(category_id, methods=['GET', 'POST']):
    """ This function shows the particular category whose
    id is given. """
    category = session.query(Category).\
        filter_by(id=category_id).one()
    item = session.query(Item).\
        filter_by(category_id=category.id)
    return render_template('item.html', category=category, item=item)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
    """ This function add's new category. """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_Category = Category(name=request.form['name'],
                                image=request.form['image'])
        session.add(new_Category)
        session.commit()
        flash('New Category created')
        return redirect(url_for('showallCategories'))
    else:
        return render_template('newCategory.html')


@app.route('/catalog/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newItem(category_id):
    """ This function add's new item to a particular Category,
    mentioned by the category id. """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            category_id=category_id)
        session.add(newItem)
        session.commit()
        flash('New Item created')
        return redirect(url_for('showCategory',
                        category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)


@app.route('/catalog/<int:category_id>/edit/',
           methods=['GET', 'POST'])
def editCategory(category_id):
    """ This function edit's a particular Category,
    mentioned by the category id. """
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category). \
        filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        if request.form['image']:
            editedCategory.image = request.form['image']
        session.add(editedCategory)
        session.commit()
        flash('Category Edit successfull')
        return redirect(url_for('showallCategories'))
    else:
        return render_template(
               'editCategory.html', category_id=category_id,
               category=editedCategory)


@app.route('/catalog/<int:category_id>/item/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    """ This function edit's a particular item specified by
    the item id and category id. """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Item Edit successfull')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template(
                'editItem.html', category_id=category_id,
                item_id=item_id, item=editedItem)


@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    """ This function delete's a particular Category
    specified by the category id. """
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).\
        filter_by(id=category_id).one()
    editedItem = session.query(Item).\
        filter_by(category_id=editedCategory.id).all()
    print editedItem
    if editedItem:
        flash('Category Deletion not possible. \
            Please delete the items in Category')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        if request.method == 'POST':
            session.delete(editedCategory)
            session.commit()
            flash('Category Deletion successfull')
            return redirect(url_for('showallCategories'))
        else:
            return render_template(
                'deleteCategory.html', category_id=category_id,
                category=editedCategory)


@app.route('/catalog/<int:category_id>/item/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    """ This function delete's a particular Item specified by the
    item id and category id. """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(editedItem)
        session.commit()
        flash('Item Deletion successfull')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template(
                'deleteItem.html', category_id=category_id,
                item_id=item_id, item=editedItem)


@app.route('/login')
def showLogin():
    """ This function is used for the login. """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """This function is used to connect to Google account. """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps
                                 ('Invalid state parameter.'), 401)
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
            json.dumps('Failed to upgrade the authorization code.'),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = \
        ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
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
            json.dumps("Token's user ID doesn't match given user ID."),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."),
            401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
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
    output += ' " style = "width: 300px; height: 300px;\
    border-radius: 150px;-webkit-border-radius: \
    150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """ This function is to logout of Google account. """
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not \
            connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps
                                 ('Failed to revoke token for given user.',
                                  400))
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    """ Create User. """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """ Get user information. """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """ Get user ID. """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':
    app.secret_key = 'amruta'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
