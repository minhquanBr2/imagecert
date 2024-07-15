import axios from "axios";
import { API_URL } from "../type/constant";

if (!API_URL) {
  throw new Error("API_URL is not defined in the cónstants file");
}

export const api_http =  axios.create({
  baseURL: API_URL,
  headers: {
    "Content-type": "application/json",
  }
});

export default api_http;