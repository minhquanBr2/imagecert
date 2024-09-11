import sys
sys.path.append("..")
import firebase_admin
import os
import json


FIREBASE_CONFIGS_PATH = os.getenv('FIREBASE_CONFIGS_PATH')
with open(FIREBASE_CONFIGS_PATH, 'r') as f:
    config_data = json.load(f)
firebaseConfigUser = config_data["firebaseConfigUser"]
firebaseConfigAdmin = config_data["firebaseConfigAdmin"]


appUser = firebase_admin.initialize_app(options=firebaseConfigUser, name='appUser')
appAdmin = firebase_admin.initialize_app(options=firebaseConfigAdmin, name='appAdmin')
