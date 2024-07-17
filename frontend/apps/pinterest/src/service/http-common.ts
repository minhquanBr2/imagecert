import axios from 'axios';
import { API_URL, AUTH_KEY, CA_URL } from '../type/constant';

if (!API_URL) {
  throw new Error('API_URL is not defined in the constants file');
}

const authData = localStorage.getItem(AUTH_KEY);
if (!authData) {
  throw new Error('Auth is not defined in the local storage');
}

const token = JSON.parse(authData).accessToken;
console.log('authData', authData, token);

export const api_http = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  },
});

export const ca_http = axios.create({
  baseURL: CA_URL,
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  },
});

;
