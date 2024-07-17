import CryptoJS from 'crypto-js';
import {ca_http} from './http-common';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';



export class SSLClient {
  sessionKey: string | null = null;
  sessionID: string | null = null;

  async startHandshake() {
    const { user } = useContext(AuthContext);
    try {

       // Store session ID and key for future requests
       this.sessionID = this.generateSessionID();

      // Step 1: ClientHello
      const clientHelloResponse = await ca_http.post('/client_hello', {
        client_hello: 'Hello from client',
        client_uid: user?.uid,
        sessionID : this.sessionID
      });

      
      // Step 2: KeyExchange (Receive CA Server's public key)
      const keyExchangeResponse = await ca_http.post('/key_exchange');
      const serverPublicKey = keyExchangeResponse.data.key_exchange;

      // Generate session key
      this.sessionKey = this.generateSessionKey();

      // Encrypt session key using server's public key
      const encryptedSessionKey = this.encryptSessionKey(this.sessionKey, serverPublicKey);

     
      await ca_http.post('/store_session_key', {
        session_id: this.sessionID,
        session_key: encryptedSessionKey,
      });

    } catch (error) {
      console.error('Handshake failed:', error);
    }
  }

  async getPublicKeyCertificate() {
    try {
      if (!this.sessionID && localStorage.getItem('sessionID')) {
        this.sessionID = localStorage.getItem('sessionID');
      }
      if (!this.sessionKey && localStorage.getItem('sessionKey')) {
        this.sessionKey = localStorage.getItem('sessionKey');
      }
      if (!this.sessionID || !this.sessionKey) {
        throw new Error('Session ID or key not found');
      }

      // Continue with secure communication using session key
      const encryptedMessage = this.encryptMessage(this.sessionKey, 'Hello server!');
      const verifyResponse = await ca_http.post('/verify', {
        session_id: this.sessionID,
        encrypted_message: encryptedMessage,
      });

      console.log('Decrypted message:', verifyResponse.data.decrypted_message);

      // Example: Access protected resource
      const protectedResourceResponse = await ca_http.get('/protected_resource', {
        headers: { 'X-Session-ID': this.sessionID },
      });
      console.log('Protected resource:', protectedResourceResponse.data);
    } catch (error) {
      console.error('Error getting public key certificate:', error);
    }
  }

  generateSessionID(): string {
    const sessionID = Math.random().toString(36).substr(2, 9); // Generate random session ID
    localStorage.setItem('sessionID', sessionID);
    return sessionID;
  }

  generateSessionKey(): string {
    const sessionKey = CryptoJS.enc.Base64.stringify(CryptoJS.lib.WordArray.random(32)); // 256-bit session key
    localStorage.setItem('sessionKey', sessionKey);
    return sessionKey;
  }

  encryptSessionKey(sessionKey: string, serverPublicKey: string): string {
    // Encrypt session key using server's public key (simplified for example)
    // Replace with actual RSA encryption using serverPublicKey
    return sessionKey; // For demonstration, we're returning the sessionKey as is.
  }

  encryptMessage(sessionKey: string, message: string): string {
    const key = CryptoJS.enc.Base64.parse(sessionKey);
    const iv = CryptoJS.enc.Utf8.parse('0123456789abcdef'); // Example IV, should be random for real applications
    const encrypted = CryptoJS.AES.encrypt(message, key, { iv: iv });
    return encrypted.toString();
  }

  decryptMessage(sessionKey: string, encryptedMessage: string): string {
    const key = CryptoJS.enc.Base64.parse(sessionKey);
    const iv = CryptoJS.enc.Utf8.parse('0123456789abcdef'); // Example IV, should be random for real applications
    const decrypted = CryptoJS.AES.decrypt(encryptedMessage, key, { iv: iv });
    return decrypted.toString(CryptoJS.enc.Utf8);
  }
}
