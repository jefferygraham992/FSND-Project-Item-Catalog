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


@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    latest_items = session.query(LegoSet)
    return render_template('showcategories.html', categories=categories, latest_items=latest_items)


@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/sets/')
def showSets(category_name):
    category = session.query(Category).filter_by(category_name=category_name).one()
    lego_set = session.query(LegoSet).filter_by(categoryName=category_name).all()
    return render_template('showsets.html', category=category, lego_set=lego_set)


@app.route('/catalog/<category_name>/<lego_set_name>/')
def showSet(category_name, lego_set_name):
    return "Information about a specific set"


@app.route('/catalog/<category_name>/<lego_set_name>/create/')
def createSet(category_name, lego_set_name):
    return "Create a new lego set"


@app.route('/catalog/<category_name>/<lego_set_name>/edit/')
def editSet(category_name, lego_set_name):
    return "Edit a new lego set"


@app.route('/catalog/<category_name>/<lego_set_name>/delete/')
def deleteSet(category_name, lego_set_name):
    return "Delete a new lego set"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
