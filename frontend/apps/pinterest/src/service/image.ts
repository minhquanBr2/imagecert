import {api_http} from './http-common';
import { API_URL, AUTH_KEY } from '../type/constant';

const uploadImage = async (imageFile: File, signature: string) => {
  const formData = new FormData();
  formData.append('signature', signature);
  formData.append('file', imageFile);

  const authData = localStorage.getItem(AUTH_KEY);
  if (!authData) {
    throw new Error('Auth is not defined in the local storage');
  }
  console.log('formData', api_http, formData);

  try {
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

export const ImageServices = {
  uploadImage,
};
