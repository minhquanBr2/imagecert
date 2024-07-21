import { AUTH_KEY } from "../type/constant";
import { base64ToArrayBuffer } from "../utils/base64ToArrayBuffer";
import { arrayBufferToBase64 } from "../utils/bufferToBase64";
import { ca_http } from "./http-common";
import IndexedDBServices from "./indexDB";
import forge from 'node-forge';

export const Challenge = async (user_public_key : ArrayBuffer) => {
  
  const pubkeyBase64 = arrayBufferToBase64(user_public_key);
  if (!sessionStorage.getItem(AUTH_KEY)) {
    return null;
  }
  const user = JSON.parse(sessionStorage.getItem(AUTH_KEY) as string);
  console.log('user_public_key', pubkeyBase64);
  const payload = {
    user_public_key: pubkeyBase64,
    user_id: user.uid
  }
  
  try {
    const response = await ca_http.post('/zkp/challenge', payload);
    if (response.status !== 200) {
      throw new Error(`Server responded with status: ${response.status}`);
    }
    console.log('challenge', response.data.challenge);
    const encryptedChallenge = base64ToArrayBuffer(response.data.challenge);
    const privateKeyArrayBuffer = await IndexedDBServices.getItem('userPrivateKeyStore', user.uid);
    const privateKey = await window.crypto.subtle.importKey(
      "pkcs8",
      privateKeyArrayBuffer,
      {
        name: "RSA-OAEP",
        hash: "SHA-256"
      },
      true,
      ["decrypt"]
    );

    const decryptedChallenge = await window.crypto.subtle.decrypt(
      {
        name: "RSA-OAEP",
      },
      privateKey,
      encryptedChallenge
    );

    const decryptedChallengeUint8 = new Uint8Array(decryptedChallenge);
    // Convert Uint8Array to base64
    const decryptedChallengeBase64 = btoa(String.fromCharCode(...decryptedChallengeUint8));
    // console.log('pubkeyBase64', pubkeyBase64);
    // console.log('decryptedChallenge', decryptedChallengeBase64);
    
    const response2 = await ca_http.post('/zkp/verify', { 
      challenge_response: decryptedChallengeBase64,
      user_id: user.uid,
      user_public_key: pubkeyBase64
    });

    // console.log('response2', response2);
    if (response2.status !== 200) {
      throw new Error(`Server responded with status: ${response2.status}`);
    }

    return response2.data;
  } catch (error) {
    console.error('Error during challenge request:', error);
    throw error;
  }
}