import os
import firebase_admin
from firebase_admin import credentials, firestore

class Database:

    def __init__(self):
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

    def getSquad(name):
        pass

    def getPlayer(name):
        pass

    