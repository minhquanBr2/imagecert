import sys
sys.path.append("..")
import firebase_admin
from credential.firebase_configs import firebaseConfigUser, firebaseConfigAdmin


appUser = firebase_admin.initialize_app(options=firebaseConfigUser, name='appUser')
appAdmin = firebase_admin.initialize_app(options=firebaseConfigAdmin, name='appAdmin')
