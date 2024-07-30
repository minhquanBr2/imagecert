import axios from 'axios';
import { AUTH_KEY } from '../type/constant';

const API_BASE_URL = 'https://104.154.115.168:8001/admin_verify';

const admin_http = axios.create({
  baseURL: API_BASE_URL,
});

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

admin_http.interceptors.request.use(
  (config) => {
    return prepareHeader(config);
  }
);



admin_http.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    console.error('API Error:', error, error.response.status, error.response.data.message);
    if (error.response.status === 401 && error.response.data.includes('expired')) {
      console.error('Token expired');
      sessionStorage.removeItem(AUTH_KEY);
      window.location.reload();
    }
    return Promise.reject(error);
  }
);



export const getPendingImages = async () => {
  const response = await admin_http.get(`${API_BASE_URL}/get_pendings`);
  return response.data;
};

export const verifyImage = async (image_id: number, admin_uid: string, result: number) => {
  const payload = {
    image_id,
    admin_uid,
    result,
  };
  console.log(payload);
  await admin_http.post(`${API_BASE_URL}/verify`, payload);
};

export const getHistory = async (userUID: string) => {
  const response = await admin_http.get(`${API_BASE_URL}/verification_history/${userUID}`);
  return response.data;
}