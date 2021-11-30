from flask import Flask, render_template, url_for, request, redirect, send_from_directory
import firebase_admin
from firebase_admin import credentials, firestore
#import pandas as pd
#import numpy as np
from scripts.dynamic_algo import DynamicAlgo
import json
import os

app = Flask(__name__, template_folder='templates')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
# hi prof callahan
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

@app.route('/_dynamic_algo', methods = ['POST'])
def run_dynamic_algo():
    #print("data received for dynamic algo")
    data = json.loads(request.form['matchup'])
    DA = DynamicAlgo(data)
    best_matchup = DA.matchup()
    return json.dumps(best_matchup)

# @app.route('/static/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
if __name__== '__main__':
    app.run('127.0.0.1', 5000, debug = True)
