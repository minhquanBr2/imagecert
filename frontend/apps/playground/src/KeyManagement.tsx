import React, { useEffect, useState } from 'react';
import KeyStore from './KeyStore';


const KeyManagement: React.FC = () => {
  const [keyName, setKeyName] = useState('');
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

    try {
      const keyPair = await window.crypto.subtle.generateKey(
        { 
            name: "RSASSA-PKCS1-v1_5", 
            modulusLength: 2048, 
            publicExponent: new Uint8Array([1, 0, 1]), 
            hash: { name: 'SHA-256' } 
        },
        true,
        ["sign", "verify"]
      );
      
      const publicKey = await window.crypto.subtle.exportKey('spki', keyPair.publicKey);
      const privateKey = await window.crypto.subtle.exportKey('pkcs8', keyPair.privateKey);

      // if (keyStore) {
      //   await keyStore.savePrivateKey(keyPair.privateKey, keyName);
      //   addToKeyList({ name: keyName, spki: publicKey });
      // }

      // Create downloadable files for user
      const publicKeyBlob = new Blob([publicKey], { type: "application/x-pem-file" });
      const privateKeyBlob = new Blob([privateKey], { type: "application/x-pem-file" });

      const publicKeyUrl = URL.createObjectURL(publicKeyBlob);
      const privateKeyUrl = URL.createObjectURL(privateKeyBlob);

      // Trigger download
      const a = document.createElement('a');
      a.href = publicKeyUrl;
      a.download = `${keyName}.publicKey`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      const b = document.createElement('a');
      b.href = privateKeyUrl;
      b.download = `${keyName}.privateKey`;
      document.body.appendChild(b);
      b.click();
      document.body.removeChild(b);
    } catch (err: any) {
      alert("Could not create and save new key pair: " + err.message);
    }
  };


  const handlePrivateKeyUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !keyName) {
      alert("Must specify a key name and select a private key file.");
      return;
    }

    try {
      const privateKeyArrayBuffer = await file.arrayBuffer();
      const privateKey = await window.crypto.subtle.importKey(
        "pkcs8",
        privateKeyArrayBuffer,
        {
          name: "RSASSA-PKCS1-v1_5",
          hash: "SHA-256"
        },
        false,
        ["sign"]
      );

      if (keyStore) {
        await keyStore.savePrivateKey(privateKey, keyName);
        alert("Private key imported and saved.");
      }
    } catch (err) {
      alert("Could not import private key: " );
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
        Key Name: <input type="text" value={keyName} onChange={(e) => setKeyName(e.target.value)} />
        <button onClick={handleCreateKeyPairClick}>Create Key Pair</button>
      </section>

      <section id="upload-private-key">
        <h1>Upload Private Key</h1>
        Key Name: <input type="text" value={keyName} onChange={(e) => setKeyName(e.target.value)} /><br />
        <input type="file" accept=".pem,.key" onChange={handlePrivateKeyUpload} />
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
