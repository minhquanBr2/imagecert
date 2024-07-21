import firebase_admin
from firebase_admin import auth
import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
from middlewares.firebase.firebase_init import appUser


def get_user_email_by_uid(uid: str) -> str:
    try:
        user = auth.get_user(uid, app=appUser)
        print(f"User: {user}")
        return user
    except Exception as e:
        print(f'Error retrieving user data: {e}')
        return None


if __name__ == "__main__":
    print(get_user_email_by_uid("2wWaDqzgs7QHUWEI7bqCLFQ5wu93"))
  