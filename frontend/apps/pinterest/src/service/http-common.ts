import axios from 'axios';
import { API_URL, AUTH_KEY, CA_URL } from '../type/constant';
import { logOutUser } from '../utils/authUtils';
import forge from 'node-forge';

if (!API_URL) {
  console.error('API_URL is not defined in the constants file');
}

const prepareHeader = (config : any) => {
  const authData = sessionStorage.getItem(AUTH_KEY);
  let token = null;

  if (authData) {
    token = JSON.parse(authData).accessToken;
  } else {
    console.error('prepareHeader: Auth is not defined in the local storage');
  }

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
};


export const api_http = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ca_http = axios.create({
  baseURL: CA_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

ca_http.interceptors.request.use(
  async (config) => {
    let sessionKey = sessionStorage.getItem('sessionKey');

    if (sessionKey) {
      console.log('REQUEST WITH ENCRYPTED');
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

    

    return prepareHeader(config);
  },
  error => Promise.reject(error)
);

ca_http.interceptors.response.use(
  response => {
    let sessionKey = sessionStorage.getItem('sessionKey');

    if (sessionKey && response.data && response.data.iv && response.data.payload && response.data.tag) {
      console.log('RESPONSE WITH DECRYPTED');
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
    console.error('API Error:', error, error.response.status, error.response.data.message);
    if (error.response.status === 401 && error.response.data.message.includes('expired')) {
      console.error('Token expired');
      logOutUser();
    }
    return Promise.reject(error);
  }
);

export default api_http;
