import './styles/normalize.css';

import FinalBoard from './components/FinalBoard';
import React, { useContext, useEffect } from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { firestore } from './firebase_setup/firebase';
import AuthContext from './context/AuthContext';
import LoginScreen from './pages/Login';
import { SSLClient } from './service/handShake';
firestore

const  App = () =>  {

  const { user } = useContext(AuthContext);
  // Challenge();
  // SSLClient.startHandshake();
  useEffect(() => {
    SSLClient.startHandshake();
  }, []);
  return (
    <React.Fragment>
      <ToastContainer/>
      {user ? <FinalBoard /> : <LoginScreen/>}
      {/* <KeyManager/> */}
    </React.Fragment>
  );
}

export default App;
