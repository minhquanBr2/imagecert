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
    // UserServices.authorizeGoogle().then((result) => {
    //   if (result.status === 1) {
    //     console.log('User signed in:', result.user);
    //     UserServices.addNewUser({firebaseUID: result.user.uid, publicKey: "publicKey", role: "role"}).then((result) => {
    //       toast.success('User added to database');
    //       setTab(1);
    //     }).catch((error) => {
    //       console.error('Error adding user to database:', error);
    //       toast.error('Error adding user to database');
    //     });
        
    //   } else {
    //     console.error('Error signing in:', result.errorMessage);
    //     toast.error('Error signing in');
    //   }
    // });
    console.log("Sign in with Google", localStorage.getItem("token"));
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
