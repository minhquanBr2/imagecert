import { API_URL, AUTH_KEY } from '../type/constant';
import api_http from './http-common';

const uploadImage = async (imageFile: File) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  const user = JSON.parse(localStorage.getItem(AUTH_KEY) as string);
  formData.append('uid', user.uid);

  return api_http.post(`${API_URL}/upload`, formData);
};

export const ImageServices = {
  uploadImage,
};
