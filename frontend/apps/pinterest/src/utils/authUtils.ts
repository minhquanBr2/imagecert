import { getAuth, signOut } from 'firebase/auth';
import { AUTH_KEY } from '../type/constant';

export const logOutUser = () => {
  const auth = getAuth();
  signOut(auth)
    .then(() => {
      console.log('User logged out due to 401 response');
      localStorage.removeItem(AUTH_KEY);
      window.location.reload(); // Optionally, reload the app to reset state
    })
    .catch((logoutError) => {
      console.log('Logout error: ', logoutError);
    });
};