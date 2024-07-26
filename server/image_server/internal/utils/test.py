
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print (sys.path)
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate('/home/khang/imagecert/server/image_server/credential/imageca-5c31b-firebase-adminsdk-cf4th-324d39aa3b.json')
firebase_admin.initialize_app(credential=cred)
from getEmailFromUid import get_user_email_by_uid
print(get_user_email_by_uid("3NmpDRZD1ugWfQrZq70OraVDzNl1"))