import { SSLClient } from "./handShake";


export const getCertForPubkey = async (pubkey: string) => {
  try{
    if (!SSLClient.sessionKey && localStorage.getItem('sessionKey')) {
      SSLClient.sessionKey = localStorage.getItem('sessionKey');
    }else if (!SSLClient.sessionKey){
      await SSLClient.startHandshake();
    }



  }catch(error){
    console.error('Error getting cert for public key:', error);
  }
}