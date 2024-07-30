import { Buffer } from 'buffer';
import IndexedDBServices from '../service/indexDB';
import { base64ToArrayBuffer } from '../utils/base64ToArrayBuffer';

class KeyManager {
  private static instance: KeyManager | null = null;

  private algoName: string;
  private hashFunction: string;

  private constructor(algoName: string, hashFunction: string) {
    this.algoName = algoName;
    this.hashFunction = hashFunction;
  }

  public static getInstance(algoName: string, hashFunction: string): KeyManager {
    if (this.instance === null) {
      this.instance = new KeyManager(algoName, hashFunction);
    }
    return this.instance;
  }


  public downloadFile(blob: Blob, filename: string) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();
  }
  

  public pemEncode(buffer: ArrayBuffer, label: string): string {
    const base64 = Buffer.from(buffer).toString('base64');
    const formatted = base64.replace(/(.{64})/g, '$1\n');
    return `-----BEGIN ${label}-----\n${formatted}\n-----END ${label}-----`;
  };


  public async generateKeyPair(userUID: string): Promise<{ publicKey: ArrayBuffer; privateKey: ArrayBuffer }> {
    try {
      const keyPair = await window.crypto.subtle.generateKey(
        {
          name: this.algoName,
          modulusLength: 2048,
          publicExponent: new Uint8Array([1, 0, 1]),
          hash: this.hashFunction,
        },
        true,
        ['sign']
      );

      // Export the keys to ArrayBuffer format
      const publicKey = await window.crypto.subtle.exportKey('spki', keyPair.publicKey);
      const privateKey = await window.crypto.subtle.exportKey('pkcs8', keyPair.privateKey);

      // Create blobs for download
      const publicKeyBlob = new Blob([publicKey], { type: 'application/x-pem-file' });
      const privateKeyBlob = new Blob([privateKey], { type: 'application/x-pem-file' });

      // Download the keys as files
      this.downloadFile(publicKeyBlob, `${userUID}.pub`);
      this.downloadFile(privateKeyBlob, `${userUID}`);

      return { publicKey, privateKey };
    } catch (error) {
      console.error('Error generating key pair:', error);
      throw error;
    }
  }
  

  public async importPrivateKey(privateKeyArrayBuffer: ArrayBuffer): Promise<CryptoKey> {
    try {
      return await window.crypto.subtle.importKey(
        'pkcs8',
        privateKeyArrayBuffer,
        {
          name: this.algoName,
          hash: this.hashFunction,
        },
        true,
        ['sign']
      );
    } catch (error) {
      console.error('Error importing private key:', error);
      throw error;
    }
  }


  public async importPublicKey(publicKeyArrayBuffer: ArrayBuffer): Promise<CryptoKey> {
    try {
      return await window.crypto.subtle.importKey(
        'spki',
        publicKeyArrayBuffer,
        {
          name: this.algoName,
          hash: this.hashFunction,
        },
        true,
        ['verify']
      );
    } catch (error) {
      console.error('Error importing public key:', error);
      throw error;
    }
  }
  

  public async signImage(userUID: string, imageFile: File): Promise<string> {
    try {
      const privateKeyData = await IndexedDBServices.getItem('userPrivateKeyStore', userUID);
      const privateKeyArrayBuffer = privateKeyData instanceof ArrayBuffer
        ? privateKeyData
        : base64ToArrayBuffer(privateKeyData);
      const privateKey = await this.importPrivateKey(privateKeyArrayBuffer);

      const arrayBuffer = await imageFile.arrayBuffer();
      const signature = await window.crypto.subtle.sign(
        this.algoName,
        privateKey,
        arrayBuffer
      );
      return Buffer.from(signature).toString('base64');
    } catch (error) {
      console.error('Error signing image:', error);
      throw error;
    }
  }
};


// Create and export the singleton instance
const keyManagerInstance = KeyManager.getInstance('RSASSA-PKCS1-v1_5', 'SHA-256');
export default keyManagerInstance;
