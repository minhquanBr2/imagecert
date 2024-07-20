import {api_http} from './http-common';
import { API_URL, AUTH_KEY, IMAGE_URL } from '../type/constant';

const uploadImage = async (imageFile: File, signature: string) => {
  const formData = new FormData();
  formData.append('signature', signature);
  formData.append('file', imageFile);

  const authData = sessionStorage.getItem(AUTH_KEY);
  if (!authData) {
    throw new Error('Auth is not defined in the local storage');
  }

  try {
    console.log('api_http', api_http);
    console.log('formData', formData);
    const response = await api_http.post(`${API_URL}/upload/image`, formData,{
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading image:', error);
    throw error;
  }
};

const getAll = async () => {
  const response = await api_http.get(`${IMAGE_URL}/select/all_images`);
  return response.data;
}

export const ImageServices = {
  uploadImage,
  getAll
};
