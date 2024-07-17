import CryptoJS from 'crypto-js';
import {ca_http} from './http-common';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';
import forge from 'node-forge';


export class SSLClient {
  sessionKey: string | null = null;
  sessionID: string | null = null;

  async startHandshake() {
    const { user } = useContext(AuthContext);
    // Store session ID and key for future requests
    this.sessionID = this.generateSessionID();

    // Step 1: ClientHello
    // console.log('ClientHello User:', user);
    const clientHelloResponse = await ca_http.post('/client_hello', {
      client_hello: 'Hello from Client',
      client_uid: user?.uid,
      sessionID : this.sessionID
    });

    if (clientHelloResponse.status !== 200) {
      throw new Error(`ClientHello failed with message: ${clientHelloResponse.data}`);
    }

    
    // Step 2: KeyExchange (Receive CA Server's public key)
    const keyExchangeResponse = await ca_http.post('/key_exchange');
    if (keyExchangeResponse.status !== 200) {
      throw new Error(`ClientHello failed with message: ${keyExchangeResponse.data}`);
    }
    const serverPublicKey = keyExchangeResponse.data.key_exchange;
    const serverPublicKey_forge = forge.pki.publicKeyFromPem(serverPublicKey);
    // console.log('Server public key:', serverPublicKey);

    // Generate session key
    this.sessionKey = this.generateSessionKey();

    const payload = {
      session_id: this.sessionID,
      session_key: this.sessionKey,
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

    // Send the encrypted payload to the server
    const storeKeyResponse = await ca_http.post('/store_session_key', {
      data: encryptedPayloadBase64,
    });

    console.log('Store Key Response:', storeKeyResponse.data);
    if (storeKeyResponse.status !== 200) {
      throw new Error(`ClientHello failed with message: ${storeKeyResponse.data}`);
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
    const publicKey = forge.pki.publicKeyFromPem(serverPublicKey);
    const encrypted = publicKey.encrypt(sessionKey, 'RSA-OAEP', {
      md: forge.md.sha256.create(),
      mgf1: forge.mgf.mgf1.create(forge.md.sha256.create())
    });
    return forge.util.encode64(encrypted);
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
