import React, { useState, useContext } from 'react';
import { Button, Container, Typography, TextField, Avatar, Paper } from '@mui/material';
import { getAuth, signInWithEmailAndPassword, UserCredential } from 'firebase/auth';
import AuthContext from '../../context/AuthContext';
import { AUTH_KEY } from '../../type/constant';
import { toast } from 'react-toastify';

const LoginScreen: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const authContext = useContext(AuthContext);
  const auth = getAuth();

  const signInWithEmailPasswordHandler = async () => {
    try {
      const userCredential : UserCredential | any = await signInWithEmailAndPassword(auth, email, password);

      const user = userCredential.user;
      const token = await user.getIdToken();

      const authData = {
        displayName: user?.displayName || '',
        email: user?.email || '',
        photoURL: user?.photoURL || '',
        uid: user?.uid || '',
        accessToken: token || '',
      };

      window.sessionStorage.setItem(AUTH_KEY, JSON.stringify(authData));
      authContext.logIn(authData);
    } catch (error: any) {
      alert(error.message);
    }
  };

  return (
    <Container
      maxWidth="sm"
      style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
    >
      <Paper elevation={3} style={{ padding: '40px', textAlign: 'center', borderRadius: '10px' }}>
        <Avatar src="/adminLogo.png" alt="Admin logo" style={{ width: 100, height: 100, margin: '0 auto 40px', padding: '10px' }} />
        <Typography variant="h4" gutterBottom>
          Sign in to ADMIN
        </Typography>
        <TextField
          label="Email"
          variant="outlined"
          fullWidth
          margin="normal"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          variant="outlined"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={signInWithEmailPasswordHandler}
          style={{ marginTop: '24px', padding: '10px 20px' }}
        >
          Sign In
        </Button>
      </Paper>
    </Container>
  );
};

export default LoginScreen;
