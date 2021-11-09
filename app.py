from flask import Flask, render_template, url_for, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
#import numpy as np
import json
import os

app = Flask(__name__, template_folder='templates')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

@app.route('/')
def hello():
     
    #firebase_key = os.environ['FIREBASE_KEY']
    #with open("tmp/firebase_key.json", "w") as f:
    #    f.write(firebase_key)
    #    cred = credentials.Certificate("firebase_key.json")
    #    firebase_admin.initialize_app(cred)
    #    db = firestore.client()

    firebase_key = {
        'type':os.environ['type'],
        'project_id':os.environ['project_id'],
        'private_key':os.environ['private_key'],
        'client_email':os.environ['client_email'],
        'token_uri':os.environ['token_uri']
    }
    cred = credentials.Certificate(firebase_key)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    #players = pd.read_csv( 'static/inhouse_positional.csv' )
    #players_json = players.to_json(orient='index')
    #parsed = json.loads( players_json )
    #with open("static/players.json", 'w') as f:
        #f.write(players_json)
        #f.close()
    
    doc_stream = db.collection(u"players").stream()
    docs = {}
    for doc in doc_stream:
        doc[doc.id] = doc.to_dict()

    return render_template('index.html', docs=docs)

if __name__== '__main__':
    app.run('127.0.0.1', 5000, debug = True)
