from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import numpy as np
import json

app = Flask(__name__, template_folder='templates')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

@app.route('/')
def hello():
    players = pd.read_csv( 'static/inhouse_positional.csv' )
    players_json = players.to_json(orient='index')
    #parsed = json.loads( players_json )
    with open("static/players.json", 'w') as f:
        f.write(players_json)
        f.close()
    return render_template('index.html', ratings=players_json)

if __name__== '__main__':
    app.run('127.0.0.1', 5000, debug = True)
