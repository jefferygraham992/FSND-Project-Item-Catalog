from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, LegoSet, User
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

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# show all Lego set categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.category_name))
    latest_items = session.query(LegoSet)
    return render_template('showcategories.html', categories=categories, latest_items=latest_items)


# show all Lego set for a particular category
@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/sets/')
def showSets(category_name):
    category = session.query(Category).filter_by(category_name=category_name).one()
    lego_set = session.query(LegoSet).filter_by(categoryName=category_name).all()
    return render_template('showsets.html', category=category, lego_set=lego_set)


# show information for a particular Lego set
@app.route('/catalog/<category_name>/<set_name>/')
def showSet(category_name, set_name):
    lego_set = session.query(LegoSet).filter_by(set_name=set_name).one()
    return render_template('showset.html', lego_set=lego_set)


# Create a new Lego set
@app.route('/catalog/<category_name>/sets/new')
def createSet(category_name):
    categories = session.query(Category).all()
    selectedCategory = category_name
    return render_template('createset.html', categories=categories, selectedCategory=selectedCategory)


# Edit a Lego set
@app.route('/catalog/<category_name>/<set_name>/edit/')
def editSet(category_name, set_name):
    lego_set = session.query(LegoSet).filter_by(set_name=set_name).one()
    categories = session.query(Category).all()
    return render_template('editset.html', lego_set=lego_set, categories=categories)


# Delete a Lego set
@app.route('/catalog/<category_name>/<set_name>/delete/')
def deleteSet(category_name, set_name):
    lego_set = session.query(LegoSet).filter_by(set_name=set_name).one()
    return render_template('deleteset.html', lego_set=lego_set)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
