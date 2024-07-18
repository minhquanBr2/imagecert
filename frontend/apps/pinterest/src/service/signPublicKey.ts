import { Challenge } from "./caChallenge";
import { SSLClient } from "./handShake";


export const getCertForPubkey = async (pubkey: string) => {
  try{
    if (!SSLClient.sessionKey && localStorage.getItem('sessionKey')) {
      SSLClient.sessionKey = localStorage.getItem('sessionKey');
    }else if (!SSLClient.sessionKey){
      await SSLClient.startHandshake();
    }

    Challenge(pubkey).then((response) => {
      console.log('response', response);
      localStorage.removeItem('sessionKey');
    localStorage.removeItem('sessionID');
    }).catch((error) => {
      console.log('error', error);
      localStorage.removeItem('sessionKey');
    localStorage.removeItem('sessionID');
    });

    

  }catch(error){
    console.error('Error getting cert for public key:', error);
  }
}