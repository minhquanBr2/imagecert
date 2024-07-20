import axios from 'axios';
import { AUTH_KEY } from '../type/constant';

const API_BASE_URL = 'http://104.154.115.168:8001/admin_verify';

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


export const getPendingImages = async () => {
  const response = await admin_http.get(`${API_BASE_URL}/get_pendings`);
  return response.data;
};

export const verifyImage = async (admin_uid: string, image_id: string, result: number) => {
  const payload = {
    admin_uid,
    image_id,
    result,
  };
  await admin_http.post(`${API_BASE_URL}/verify`, payload);
};