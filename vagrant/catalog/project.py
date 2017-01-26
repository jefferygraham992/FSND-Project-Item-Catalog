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
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON APIs
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/catalog/<category_name>/JSON')
@app.route('/catalog/<category_name>/sets/JSON')
def showSetsJSON(category_name):
    category = session.query(Category).filter_by(category_name=category_name).one()
    lego_sets = session.query(LegoSet).filter_by(categoryName=category_name).all()
    return jsonify(LegoSet=[lego_set.serialize for lego_set in lego_sets])


@app.route('/catalog/<category_name>/<set_name>/JSON')
def showSetJSON(category_name, set_name):
    lego_set = session.query(LegoSet).filter_by(set_name=set_name).one()
    return jsonify(lego_set=lego_set.serialize)


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
    lego_sets = session.query(LegoSet).filter_by(categoryName=category_name).all()
    return render_template('showsets.html', category=category, lego_sets=lego_sets)


# show information for a particular Lego set
@app.route('/catalog/<category_name>/<set_name>/')
def showSet(category_name, set_name):
    lego_set = session.query(LegoSet).filter_by(set_name=set_name).one()
    return render_template('showset.html', lego_set=lego_set)


# Create a new Lego set
@app.route('/catalog/<category_name>/sets/new', methods=['GET', 'POST'])
def createSet(category_name):
    categories = session.query(Category).all()
    selectedCategory = category_name
    category = session.query(Category).filter_by(category_name=category_name).one()
    if request.method == 'POST':
        newSet = LegoSet(set_name=request.form['set_name'],
                                    pieces=request.form['pieces'],
                                    set_id=request.form['set_id'],
                                    description=request.form['description'],
                                    set_picture=request.form['set_picture'],
                                    categoryName=request.form['category_name'])
        session.add(newSet)
        session.commit()
        return redirect(url_for('showSets', category_name=category_name))
    else:
        return render_template('createset.html', categories=categories, selectedCategory=selectedCategory)


# Edit a Lego set
@app.route('/catalog/<category_name>/<set_name>/edit/', methods=['GET', 'POST'])
def editSet(category_name, set_name):
    editedSet = session.query(LegoSet).filter_by(set_name=set_name).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        if request.form['set_name']:
            editedSet.set_name = request.form['set_name']
        if request.form['description']:
            editedSet.description = request.form['description']
        if request.form['set_id']:
            editedSet.set_id = request.form['set_id']
        if request.form['pieces']:
            editedSet.pieces = request.form['pieces']
        if request.form['categoryName']:
            editedSet.categoryName = request.form['categoryName']
        session.add(editedSet)
        session.commit()
        return redirect(url_for('showSets', category_name=category_name))
    else:
        return render_template('editset.html', lego_set=editedSet, categories=categories)


# Delete a Lego set
@app.route('/catalog/<category_name>/<set_name>/delete/', methods=['GET', 'POST'])
def deleteSet(category_name, set_name):
    lego_set = session.query(LegoSet).filter_by(set_name=set_name).one()
    setToDelete = session.query(LegoSet).filter_by(set_name=set_name).one()
    if request.method == 'POST':
        session.delete(setToDelete)
        session.commit()
        return redirect(url_for('showSets', category_name=category_name))
    else:
        return render_template('deleteset.html', lego_set=lego_set)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
