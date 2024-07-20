// src/App.tsx

import React from 'react';
import './styles/App.css';
import Dashboard from './components/DashBoard';
import { useEffect } from 'react';
import UserServices from './services/user';
import { toast } from 'react-toastify';

const App: React.FC = () => {
  // const nav = useNavigate();
  const [tab, setTab] = React.useState(0);
  const handleSignIn = () => {
    console.log("Sign in", sessionStorage.getItem("token"));
  };
  useEffect(() => {
    console.log(tab);
  }, [tab]);

  return (
    <React.Fragment>
    <button style={{color: "wheat", width:"300px"}} onClick={handleSignIn}>Sign in with Google</button>
    {tab >= 1 && <Dashboard />}
    {tab === 0 && <div>Not signed in</div>}
    </React.Fragment>
  );
};

export default App;
