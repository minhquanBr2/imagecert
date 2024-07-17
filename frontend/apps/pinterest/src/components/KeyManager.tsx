import React, { useState } from 'react';
import { Crypto } from '@peculiar/webcrypto';

const KeyManager: React.FC = () => {
  const [publicKeyPem, setPublicKeyPem] = useState<string>('');
  const [privateKeyPem, setPrivateKeyPem] = useState<string>('');

  const generateKeyPair = async () => {
    const crypto = new Crypto();
    const keyPair = await crypto.subtle.generateKey(
      {
        name: 'RSASSA-PKCS1-v1_5',
        modulusLength: 2048,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: 'SHA-256'
      },
      true,
      ['sign', 'verify']
    );

    const publicKey = await crypto.subtle.exportKey('spki', keyPair.publicKey);
    const privateKey = await crypto.subtle.exportKey('pkcs8', keyPair.privateKey);

    setPublicKeyPem(pemEncode(publicKey, 'PUBLIC KEY'));
    setPrivateKeyPem(pemEncode(privateKey, 'PRIVATE KEY'));
  };

  const pemEncode = (buffer: ArrayBuffer, label: string) => {
    const base64 = Buffer.from(buffer).toString('base64');
    const formatted = base64.replace(/(.{64})/g, '$1\n');
    return `-----BEGIN ${label}-----\n${formatted}\n-----END ${label}-----`;
  };

  const handleGenerateKeys = async () => {
    await generateKeyPair();
  };

  return (
    <div>
      <button onClick={handleGenerateKeys}>Generate Keys</button>
      {publicKeyPem && <pre>{publicKeyPem}</pre>}
      {privateKeyPem && <pre>{privateKeyPem}</pre>}
    </div>
  );
};

export default KeyManager;
