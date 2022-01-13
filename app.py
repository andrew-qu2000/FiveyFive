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
# test with no heroku action, no wait for CI, automatic deploy on
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
    # get position labels
    # hardcoded for LoL settings for now
    game_ref = db.collection(u"game_setup").document(u"league_of_legends")
    game_dict = game_ref.get().to_dict()
    positions = game_dict['position_labels']
    weights = game_dict['rating_weights']
    return render_template('index.html', docs=docs, positions=positions, weights=weights)

@app.route('/_dynamic_algo', methods = ['POST'])
def run_dynamic_algo():
    #print("data received for dynamic algo")
    data = json.loads(request.form['matchup'])
    positions = request.form.getlist('positions[]')
    # is there any other standard for this casting?
    weights = [float(k) for k in request.form.getlist('weights[]')]
    from_random = request.form['fromRandom']
    DA = DynamicAlgo(data, positions, weights)
    # weird line cause of js true vs python True
    best_matchup = DA.matchup(from_random == 'true')
    ratings = DA.determine_ratings(best_matchup)
    margin = DA.calc_margin(ratings)
    return json.dumps(best_matchup)

# @app.route('/static/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
if __name__== '__main__':
    app.run('127.0.0.1', 5000, debug = True)
