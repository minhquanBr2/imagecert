import { AUTH_KEY } from "../type/constant";
import { ca_http } from "./http-common";

export const Challenge = async (user_public_key : string) => {
  if (!localStorage.getItem(AUTH_KEY)) {
    return null;
  }
  const user = JSON.parse(localStorage.getItem(AUTH_KEY) as string);
  const payload = {
    user_public_key: "user_public_key",
    user_id: user.uid
  }
  const response = await ca_http.post('/zkp/challenge', payload);
  console.log('response', response);
  return response.data;
}