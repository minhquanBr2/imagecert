import { Buffer } from 'buffer';
import IndexedDBServices from '../service/indexDB';

class KeyManager {

  public static pemEncode(buffer: ArrayBuffer, label: string): string {
    const base64 = Buffer.from(buffer).toString('base64');
    const formatted = base64.replace(/(.{64})/g, '$1\n');
    return `-----BEGIN ${label}-----\n${formatted}\n-----END ${label}-----`;
  };

  public static async generateKeyPair(): Promise<{ publicKey: ArrayBuffer; privateKey: ArrayBuffer }> {
    const keyPair = await window.crypto.subtle.generateKey(
      {
        name: 'RSASSA-PKCS1-v1_5',
        modulusLength: 2048,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: 'SHA-256'
      },
      true,
      ['sign', 'verify']
    );

    
    // publicKey và privateKey đang có kiểu Crypto, nếu muốn chuyển về kiểu ArrayBuffer thì uncomment 2 dòng 26 27 và comment lại dòng 28 29
    const publicKey = await window.crypto.subtle.exportKey('spki', keyPair.publicKey);
    const privateKey = await window.crypto.subtle.exportKey('pkcs8', keyPair.privateKey);
    // const publicKey = keyPair.publicKey;
    // const privateKey = keyPair.privateKey;
    // phải export key mới download được

    // ko cần chuyển về pem, để private key và public key ở kiểu Crypto mới đưa vô thực hiện các thao tác sign và verify đc
    // const publicKeyPem = this.pemEncode(publicKey, 'PUBLIC KEY');
    // const privateKeyPem = this.pemEncode(privateKey, 'PRIVATE KEY');

    return { publicKey, privateKey };
  }
  

  public static async importKey(privateKeyArrayBuffer: ArrayBuffer): Promise<{ privateKey: CryptoKey }> {
    const privateKey = await window.crypto.subtle.importKey(
      "pkcs8",
      privateKeyArrayBuffer,
      {
        name: "RSASSA-PKCS1-v1_5",
        hash: "SHA-256"
      },
      false,
      ["sign", "verify"]
    );
    return { privateKey };
  };


  public static async signImage(userUID: string, imageFile: File): Promise<string> {
    const privateKey = await IndexedDBServices.getItem("userPrivateKeyStore", userUID as string);
    const arrayBuffer = await imageFile.arrayBuffer();  
    const signature = await window.crypto.subtle.sign(
      'RSASSA-PKCS1-v1_5',
      privateKey,
      arrayBuffer
    );
    return Buffer.from(signature).toString('base64');
  }

};

export default KeyManager;