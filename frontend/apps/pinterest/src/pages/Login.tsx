import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';
import { signInWithPopup, GoogleAuthProvider, getAuth } from 'firebase/auth';
import './Login.css';
import { AUTH_KEY } from '../type/constant';

const LoginScreen: React.FC = () => {
  const authContext = useContext(AuthContext);
  const auth = getAuth();
  const googleProvider = new GoogleAuthProvider();

  const signInWithGoogleHandler = () => {
    signInWithPopup(auth, googleProvider)
      .then((result) => {
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const token = credential?.accessToken;
        const user = result.user;

        console.log('user', user);

        const authData = {
          displayName: user?.displayName || '',
          email: user?.email || '',
          photoURL: user?.photoURL || '',
          uid: user?.uid || '',
          accessToken: token || '',
          // refreshToken: '',
        };

        try {
          window.localStorage.setItem(AUTH_KEY, JSON.stringify(authData));
        } catch (err) {
          console.error('Error saving auth to local storage', err);
        }

        authContext.logIn(authData);
      })
      .catch((error) => {
        const errorMessage = error.message;
        alert(errorMessage);
      });
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <img
          src="https://cdn.worldvectorlogo.com/logos/pinterest-1.svg"
          alt="Pinterest logo"
        />
        <div className="login-text">
          <h2>Sign in to Pinterest</h2>
        </div>
        <button onClick={signInWithGoogleHandler} className="login-button">
          Sign In With Google
        </button>
      </div>
    </div>
  );
};

export default LoginScreen;
