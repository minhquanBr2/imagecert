import React, { useEffect, useState } from 'react';
import KeyStore from './KeyStore';

const KeyManagement: React.FC = () => {
  const [keyName, setKeyName] = useState('');
  const [keyType, setKeyType] = useState('');
  const [keyStore, setKeyStore] = useState<KeyStore | null>(null);
  const [keys, setKeys] = useState<{ name: string, spki: string }[]>([]);

  useEffect(() => {
    const ks = new KeyStore();
    ks.open()
      .then(() => {
        setKeyStore(ks);
        populateKeyListing(ks);
      })
      .catch(err => {
        alert("Could not open key store: " + err.message);
      });
  }, []);

  const populateKeyListing = (keyStore: KeyStore) => {
    keyStore.listKeys()
      .then(list => {
        setKeys(list.map(item => ({ name: item.value.name, spki: createDataUrlFromByteArray(new Uint8Array(item.value.spki)) })));
      })
      .catch(err => {
        alert("Could not list keys: " + err.message);
      });
  };

  const handleCreateKeyPairClick = async () => {
    if (!keyName) {
      alert("Must specify a name for the new key.");
      return;
    }

    if (!keyType) {
      alert("Must select kind of key first.");
      return;
    }
    
    const algorithm = keyType === 'Signing' ? 'RSASSA-PKCS1-v1_5' : 'RSA-OAEP';
    const usages = keyType === 'Signing' ? ['sign', 'verify'] : ['encrypt', 'decrypt'];
    const keyUsages: KeyUsage[] = usages.map((usage: string) => usage as KeyUsage);


    try {
      const keyPair = await window.crypto.subtle.generateKey(
        { 
            name: algorithm, 
            modulusLength: 2048, 
            publicExponent: new Uint8Array([1, 0, 1]), 
            hash: { name: 'SHA-256' } 
        },
        false,
        keyUsages
      );

      if (keyStore) {
        await keyStore.saveKey(keyPair.publicKey, keyPair.privateKey, keyName);
        addToKeyList({ name: keyName, spki: await window.crypto.subtle.exportKey('spki', keyPair.publicKey) });
      }
    } catch (err) {
      alert("Could not create and save new key pair: " + err.message);
    }
  };

  const addToKeyList = (savedObject: { name: string, spki: ArrayBuffer }) => {
    setKeys([...keys, { name: savedObject.name, spki: createDataUrlFromByteArray(new Uint8Array(savedObject.spki)) }]);
  };

  const createDataUrlFromByteArray = (byteArray: Uint8Array) => {
    let binaryString = '';
    for (let i = 0; i < byteArray.byteLength; i++) {
      binaryString += String.fromCharCode(byteArray[i]);
    }
    return "data:application/octet-stream;base64," + btoa(binaryString);
  };

  return (
    <div>
      <h1>Key Management</h1>
      <section id="create-keys">
        <h1>Create New Key Pair</h1>
        Key Name: <input type="text" value={keyName} onChange={(e) => setKeyName(e.target.value)} /><br />
        Purpose:
        <input type="radio" name="created-key-type" value="Signing" onChange={() => setKeyType('Signing')} />Signing
        <input type="radio" name="created-key-type" value="Encrypting" onChange={() => setKeyType('Encrypting')} />Encrypting
        <br />
        <button onClick={handleCreateKeyPairClick}>Create Key Pair</button>
      </section>

      <section id="list-keys">
        <h1>Stored Keys</h1>
        <ul>
          {keys.map((key, index) => (
            <li key={index}>
              <a download={`${key.name}.publicKey`} href={key.spki}>{key.name}</a>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default KeyManagement;
