import firebase_admin
from firebase_admin import auth

def get_user_email_by_uid(uid: str) -> str:
    try:
        user = auth.get_user(uid)
        return user.email
    except firebase_admin.auth.AuthError as e:
        print(f"Error fetching user data: {e}")
        return None
  