# imagecert
An image registration system for images of multiple categories, based on the principles of Certificate Authority

### 1. Deployment
#### 1a. Server
- Switch to branch `docker`.
- `cd server`
- Create `secrets` directory under `server` and add necessary files.
- Run `docker compose up --build`
#### 1b. Client
- The 2 websites (one for normal users, one for administrators) are hosted with Firebase hosting.
- User website: https://imageca-5c31b.web.app/
- Admin website: https://imageca-6c45f.web.app/

### 2. Usage
#### 2a. User website
- First, sign in with a Google account.
- When an account is signed in for the first time, the website requires the user to either generate a key pair (1) or to upload a generated key pair (2). If you want to generate a key pair, please enable the browser to download multiple times.
- The key pair will be stored in browser's IndexedDB.
#### 2b. Admin website
- Use an email and password to sign in into the website.
