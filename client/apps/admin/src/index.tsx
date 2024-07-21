import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { firestore } from './firebase/settup';
import { AuthProvider } from './context/AuthContext';
firestore
const rootEl = document.getElementById('root');
if (rootEl) {
  const root = ReactDOM.createRoot(rootEl);
  root.render(
    <React.StrictMode>
      <AuthProvider>
      <App />
      </AuthProvider>
    </React.StrictMode>,
  );
}
