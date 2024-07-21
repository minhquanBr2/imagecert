import { toast } from "react-toastify";
import { AUTH_KEY } from "../type/constant";
import { arrayBufferToBase64 } from "../utils/bufferToBase64";
import { Challenge } from "./caChallenge";
import { SSLClient } from "./handShake";
import IndexedDBServices from "./indexDB";


export const getCertForPubkey = async () => {
  try{
    if (!SSLClient.sessionKey && sessionStorage.getItem('sessionKey')) {
      SSLClient.sessionKey = sessionStorage.getItem('sessionKey');
    }else if (!sessionStorage.getItem('sessionKey')){
      await SSLClient.startHandshake();
    }

    if (!sessionStorage.getItem('sessionKey')){
      toast.error('Session key not found in local storage');
      return 0;
    }
    
    const user = JSON.parse(sessionStorage.getItem(AUTH_KEY) as string);    
    const publicKey : ArrayBuffer = await IndexedDBServices.getItem('userPublicKeyStore', user.uid);
    
    const result =  await Challenge(publicKey);

    if (result){
      sessionStorage.removeItem('sessionKey');
      sessionStorage.removeItem('sessionID');
      return 1;
    }else{
      sessionStorage.removeItem('sessionKey');
      sessionStorage.removeItem('sessionID');
      return 0;
    }
  }catch(error){
    console.error('Error getting cert for public key:', error);
    return 0;
  }
}