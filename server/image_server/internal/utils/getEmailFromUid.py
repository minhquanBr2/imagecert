import firebase_admin
from firebase_admin import auth
import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
from middlewares.firebase.firebase_init import appUser, appAdmin


print(appAdmin.credential)
print(appAdmin.name)
print(appAdmin.project_id)


def get_user_email_by_uid(uid: str) -> str:
    try:
        user = auth.get_user(uid=uid, app=appAdmin)
        print(f"User: {user}")
        return user
    except Exception as e:
        print(f'Error retrieving user data: {e}')
        return 'x'
  