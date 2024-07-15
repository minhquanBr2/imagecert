import './styles/normalize.css';

import FinalBoard from './components/FinalBoard';
import React from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { firestore } from './firebase_setup/firebase';
firestore
function App() {
  return (
    <React.Fragment>
      <ToastContainer/>
      <FinalBoard />
    </React.Fragment>
  );
}

export default App;
