TEMP_IMAGE_DIR = "/data/images/temp"    
PERM_IMAGE_DIR = "/data/images/perm"             

# Verification status
VERIFICATION_STATUS = {
    "ACCEPTED": 0,
    "PENDING": 1,
    "REJECTED": 2
}

# Verification status mapping because the frontend and backend have different values for the verification status
VERIFICATION_STATUS_FE_BE_MAPPING = {
    1: 0,
    0: 2
}

# DB endpoint
DB_ENDPOINT_URL = "http://localhost:8003"

# Client app for users
CLIENT_APP_USER = "https://imageca-5c31b.web.app"

# Mail compose
MAIL_COMPOSE_URL = "https://mail.google.com/mail/u/0/#inbox?compose=new"