import { AUTH_KEY } from "../type/constant";
import { arrayBufferToBase64 } from "../utils/bufferToBase64";
import { Challenge } from "./caChallenge";
import { SSLClient } from "./handShake";
import IndexedDBServices from "./indexDB";


export const getCertForPubkey = async (pubkey: string) => {
  try{
    if (!SSLClient.sessionKey && sessionStorage.getItem('sessionKey')) {
      SSLClient.sessionKey = sessionStorage.getItem('sessionKey');
    }else if (!SSLClient.sessionKey){
      await SSLClient.startHandshake();
    }

    if (!sessionStorage.getItem('sessionKey')){
      return;
    }

    const user = JSON.parse(sessionStorage.getItem(AUTH_KEY) as string);

    const publicKey = await IndexedDBServices.getItem('userPublicKeyStore', user.uid);

    Challenge(publicKey).then((response) => {
      console.log('getCertForPubkey response', response);
      // sessionStorage.removeItem('sessionKey');
      // sessionStorage.removeItem('sessionID');
    }).catch((error) => {
      console.log(' getCertForPubkey error', error);
      // sessionStorage.removeItem('sessionKey');
      // sessionStorage.removeItem('sessionID');
    });

    

  }catch(error){
    console.error('Error getting cert for public key:', error);
  }
}