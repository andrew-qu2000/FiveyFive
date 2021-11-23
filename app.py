from flask import Flask, render_template, url_for, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore
#import pandas as pd
#import numpy as np
#import json
import os

app = Flask(__name__, template_folder='templates')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

firebase_key = {
    'type':os.environ['type'],
    'project_id':os.environ['project_id'],
    'private_key':os.environ['private_key'].replace('\\n', '\n'),
    'client_email':os.environ['client_email'],
    'token_uri':os.environ['token_uri']
}
cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def hello():
    """Load home page using dict of players from database"""
    doc_stream = db.collection(u"players").stream()
    docs = {}
    for doc in doc_stream:
        docs[doc.id] = doc.to_dict()

    return render_template('index.html', docs=docs)

if __name__== '__main__':
    app.run('127.0.0.1', 5000, debug = True)
