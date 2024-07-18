import axios from 'axios';
import { API_URL, AUTH_KEY, CA_URL } from '../type/constant';
import { logOutUser } from '../utils/authUtils';
import forge from 'node-forge';
import { SSLClient } from './handShake';

if (!API_URL) {
  console.error('API_URL is not defined in the constants file');
}

const authData = localStorage.getItem(AUTH_KEY);
let token = null;

if (authData) {
  token = JSON.parse(authData).accessToken;
  console.log('authData', authData, token);
} else {
  console.error('Auth is not defined in the local storage');
}

export const api_http = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    Authorization: token ? `Bearer ${token}` : '',
  },
});

export const ca_http = axios.create({
  baseURL: CA_URL,
  headers: {
    'Content-Type': 'application/json',
    Authorization: token ? `Bearer ${token}` : '',
  },
});

ca_http.interceptors.request.use(
  async (config) => {
    let sessionKey = localStorage.getItem('sessionKey');
    console.log('sessionKey', sessionKey);

    if (!sessionKey) {
      await SSLClient.startHandshake();
      sessionKey = SSLClient.getSessionKey();
    }

    if (sessionKey) {
      const payloadString = JSON.stringify(config.data);
      const iv = forge.random.getBytesSync(12);
      const cipher = forge.cipher.createCipher('AES-GCM', forge.util.decode64(sessionKey));
      cipher.start({ iv });
      cipher.update(forge.util.createBuffer(payloadString, 'utf8'));
      cipher.finish();

      const encryptedPayload = cipher.output.bytes();
      const tag = cipher.mode.tag.bytes();

      config.data = {
        iv: forge.util.encode64(iv),
        payload: forge.util.encode64(encryptedPayload),
        tag: forge.util.encode64(tag)
      };
    }

    return config;
  },
  error => Promise.reject(error)
);

ca_http.interceptors.response.use(
  response => {
    let sessionKey = localStorage.getItem('sessionKey');

    if (sessionKey && response.data && response.data.iv && response.data.payload && response.data.tag) {
      const iv = forge.util.decode64(response.data.iv);
      const encryptedPayload = forge.util.decode64(response.data.payload);
      const tag = forge.util.decode64(response.data.tag);

      const decipher = forge.cipher.createDecipher('AES-GCM', forge.util.decode64(sessionKey));
      decipher.start({ iv, tag: forge.util.createBuffer(tag) });
      decipher.update(forge.util.createBuffer(encryptedPayload));
      const success = decipher.finish();

      if (success) {
        response.data = JSON.parse(decipher.output.toString());
      } else {
        console.error('Failed to decrypt response data.');
        return Promise.reject(new Error('Failed to decrypt response data.'));
      }
    }

    return response;
  },
  error => {
    console.error('API Error:', error);
    if (error.response.status === 401 && error.response.data.detail.includes('expired')) {
      logOutUser();
    }
    return Promise.reject(error);
  }
);

export default api_http;
