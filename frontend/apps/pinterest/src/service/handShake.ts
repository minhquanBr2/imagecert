import CryptoJS from 'crypto-js';
import {ca_http} from './http-common';
import AuthContext from '../context/AuthContext';
import forge from 'node-forge';
import { AUTH_KEY } from '../type/constant';


export class SSLClient {
  static sessionKey: string | null = null;
  static sessionID: string | null = null;
  

  static async startHandshake() {
    if (localStorage.getItem('sessionKey')) {
      console.info('Session key found in local storage');
      return;
    }
    try{
      const user = JSON.parse(localStorage.getItem(AUTH_KEY) as string);
      // Store session ID and key for future requests
      SSLClient.sessionID = SSLClient.generateSessionID();

      // Step 1: ClientHello
      // console.log('ClientHello User:', user);
      const clientHelloResponse = await ca_http.post('/handshake/client_hello', {
        client_hello: 'Hello from Client',
        client_uid: user?.uid,
        sessionID : SSLClient.sessionID
      });

      if (clientHelloResponse.status !== 200) {
        throw new Error(`ClientHello failed with message: ${clientHelloResponse.data}`);
      }

      
      // Step 2: KeyExchange (Receive CA Server's public key)
      const keyExchangeResponse = await ca_http.post('/handshake/key_exchange');
      if (keyExchangeResponse.status !== 200) {
        throw new Error(`ClientHello failed with message: ${keyExchangeResponse.data}`);
      }
      const serverPublicKey = keyExchangeResponse.data.key_exchange;
      const serverPublicKey_forge = forge.pki.publicKeyFromPem(serverPublicKey);
      // console.log('Server public key:', serverPublicKey);

      // Generate session key
      SSLClient.sessionKey = SSLClient.generateSessionKey();

      const payload = {
        session_id: SSLClient.sessionID,
        session_key: SSLClient.sessionKey,
        client_uid: user?.uid,
      };

      // Convert the payload to a JSON string
      const payloadString = JSON.stringify(payload);

      // Encrypt the entire payload with the server's public key
      const encryptedPayload = serverPublicKey_forge.encrypt(payloadString, 'RSA-OAEP', {
        md: forge.md.sha256.create(),
        mgf1: forge.mgf.mgf1.create(forge.md.sha256.create()),
      });

      // Convert the encrypted payload to base64
      const encryptedPayloadBase64 = forge.util.encode64(encryptedPayload);
      // console.log('Encrypted payload:', encryptedPayloadBase64);

      // Send the encrypted payload to the server
      const storeKeyResponse = await ca_http.post('/handshake/store_session_key', {
        data: encryptedPayloadBase64,
      });

      console.log('Store Key Response:', storeKeyResponse.data);
      if (storeKeyResponse.status !== 200) {
        console.error(`ClientHello failed with message: ${storeKeyResponse.data}`);
      }else{
        localStorage.setItem('sessionKey', SSLClient.sessionKey);
      }
    }catch(error){
      console.error('Error starting handshake:', error);
    }
  }

  static async getPublicKeyCertificate() {
    try {
      if (!SSLClient.sessionID && localStorage.getItem('sessionID')) {
        SSLClient.sessionID = localStorage.getItem('sessionID');
      }
      if (!SSLClient.sessionKey && localStorage.getItem('sessionKey')) {
        SSLClient.sessionKey = localStorage.getItem('sessionKey');
      }
      if (!SSLClient.sessionID || !SSLClient.sessionKey) {
        throw new Error('Session ID or key not found');
      }

      // Continue with secure communication using session key
      const encryptedMessage = SSLClient.encryptMessage(SSLClient.sessionKey, 'Hello server!');
      const verifyResponse = await ca_http.post('/verify', {
        session_id: SSLClient.sessionID,
        encrypted_message: encryptedMessage,
      });

      console.log('Decrypted message:', verifyResponse.data.decrypted_message);

      // Example: Access protected resource
      const protectedResourceResponse = await ca_http.get('/protected_resource', {
        headers: { 'X-Session-ID': SSLClient.sessionID },
      });
      console.log('Protected resource:', protectedResourceResponse.data);
    } catch (error) {
      console.error('Error getting public key certificate:', error);
    }
  }

  static generateSessionID(): string {
    const sessionID = Math.random().toString(36).substr(2, 9); // Generate random session ID
    localStorage.setItem('sessionID', sessionID);
    return sessionID;
  }

  static generateSessionKey(): string {
    const sessionKey = CryptoJS.enc.Base64.stringify(CryptoJS.lib.WordArray.random(32)); // 256-bit session key
    SSLClient.sessionKey = sessionKey;
    return sessionKey;
  }

  static encryptSessionKey(sessionKey: string, serverPublicKey: string): string {
    const publicKey = forge.pki.publicKeyFromPem(serverPublicKey);
    const encrypted = publicKey.encrypt(sessionKey, 'RSA-OAEP', {
      md: forge.md.sha256.create(),
      mgf1: forge.mgf.mgf1.create(forge.md.sha256.create())
    });
    return forge.util.encode64(encrypted);
  }

  static encryptMessage(sessionKey: string, message: string): string {
    const key = CryptoJS.enc.Base64.parse(sessionKey);
    const iv = CryptoJS.enc.Utf8.parse('0123456789abcdef'); // Example IV, should be random for real applications
    const encrypted = CryptoJS.AES.encrypt(message, key, { iv: iv });
    return encrypted.toString();
  }

  static decryptMessage(sessionKey: string, encryptedMessage: string): string {
    const key = CryptoJS.enc.Base64.parse(sessionKey);
    const iv = CryptoJS.enc.Utf8.parse('0123456789abcdef'); // Example IV, should be random for real applications
    const decrypted = CryptoJS.AES.decrypt(encryptedMessage, key, { iv: iv });
    return decrypted.toString(CryptoJS.enc.Utf8);
  }

  static getSessionKey() {
    if (!SSLClient.sessionKey) {
      SSLClient.sessionKey = localStorage.getItem('sessionKey');
    }
    if (!localStorage.getItem('sessionKey')) {
      throw new Error('Session key not found');
    }
    return SSLClient.sessionKey || forge.util.decode64(localStorage.getItem('sessionKey') as string);
  }
}
