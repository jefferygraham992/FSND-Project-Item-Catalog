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

# Connect to Database and create database session
engine = create_engine('sqlite:///thomascatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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
    return render_template('showcatalog.html', inventory=inventory, latest_trains=latest_trains)


# show all trains in one category
@app.route('/catalog/<train_type>')
@app.route('/catalog/<train_type>/trains')
def showTrains(train_type):
    inventory = session.query(CharacterType).all()
    trainType = session.query(CharacterType).filter_by(type_name=train_type).one()
    trains = session.query(Character).filter_by(character_kind=train_type).all()
    return render_template('showtrains.html', trainType=trainType, trains=trains, inventory=inventory)


# show info for one train
@app.route('/catalog/<train_type>/<train_name>')
def showTrain(train_type, train_name):
    train = session.query(Character).filter_by(character_name=train_name).one()
    return render_template('showtrain.html', train=train)


# add a train
@app.route('/catalog/add', methods=['GET', 'POST'])
def addTrain():
    inventory = session.query(CharacterType).all()
    if request.method == 'POST':
        newTrain = Character(character_name=request.form['character_name'], description=request.form['description'], character_kind=request.form['character_kind'], character_picture=request.form['character_picture'])
        session.add(newTrain)
        flash('%s successfully added!' % newTrain.character_name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newtrain.html', inventory=inventory)


# edit a train
@app.route('/catalog/<train_name>/edit', methods=['GET', 'POST'])
def editTrain(train_name):
    inventory = session.query(CharacterType).all()
    editedTrain = session.query(Character).filter_by(character_name=train_name).one()
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
    trainToDelete = session.query(Character).filter_by(character_name=train_name).one()
    if request.method == 'POST':
        session.delete(trainToDelete)
        flash('%s successfuly deleted!' % trainToDelete.character_name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deletetrain.html', trainToDelete=trainToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
