from firebase_admin import auth, get_app
import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

# print(dir(appUser))
# print(appUser.credential.get_credential())
# print(appUser.name)
# print(appUser.project_id)


def get_user_email_by_uid(uid: str) -> str:
    try:
        user = auth.get_user(uid=uid, app=get_app("appUserSDK"))
        print(f"User: {user.email}")
        return user.email
    except Exception as e:
        print(f'Error retrieving user data: {e}')
        return None
    

  