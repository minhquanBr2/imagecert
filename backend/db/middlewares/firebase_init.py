import sys
sys.path.append("..")
import firebase_admin
from credential.firebase_config import firebaseConfig

def initialize_firebase():
    firebase_admin.initialize_app(options=firebaseConfig)
