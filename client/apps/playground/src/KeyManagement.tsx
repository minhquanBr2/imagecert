import React, { useEffect, useState } from 'react';
import KeyStore from './KeyStore';


// // Function to convert ArrayBuffer to Base64 string
// function arrayBufferToBase64(buffer: ArrayBuffer) {
//   const binary = String.fromCharCode(...new Uint8Array(buffer));
//   return window.btoa(binary);
// }


// // Function to convert the exported keys to PEM format
// function toPem(key: ArrayBuffer, type: string) {
//   const base64Key = arrayBufferToBase64(key);
//   let pem = "";
  
//   if (type === "public") {
//     pem += "-----BEGIN PUBLIC KEY-----\n";
//   } else if (type === "private") {
//     pem += "-----BEGIN PRIVATE KEY-----\n";
//   }
  
//   const lines = base64Key.match(/.{1,64}/g) || [];          // Split the base64 string into lines of 64 characters
//   pem += lines.join("\n");
  
//   if (type === "public") {
//     pem += "\n-----END PUBLIC KEY-----";
//   } else if (type === "private") {
//     pem += "\n-----END PRIVATE KEY-----";
//   }
  
//   return pem;
// }


// Function to trigger download file
function downloadFile(blob: Blob, filename: string) {
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




const KeyManagement: React.FC = () => {
  const [userUID, setUserUID] = useState('');
  const [keyStore, setKeyStore] = useState<KeyStore | null>(null);
  // const [keys, setKeys] = useState<{ name: string, spki: string }[]>([]);
  const [hasPrivateKey, setHasPrivateKey] = useState(false);

  useEffect(() => {
    const ks = new KeyStore();
    ks.open()
      .then(() => {
        setKeyStore(ks);
        // populateKeyListing(ks);
      })
      .catch(err => {
        alert("Could not open key store: " + err.message);
      });
  }, []);


  // const populateKeyListing = (keyStore: KeyStore) => {
  //   keyStore.listKeys()
  //     .then(list => {
  //       setKeys(list.map(item => ({ name: item.value.name, spki: createDataUrlFromByteArray(new Uint8Array(item.value.spki)) })));
  //     })
  //     .catch(err => {
  //       alert("Could not list keys: " + err.message);
  //     });
  // };


  const handleCreateKeyPairClick = async () => {
    if (!userUID) {
      alert("No user has been authorized.");
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

      // const publicKeyPem = toPem(publicKey, "public");
      // const privateKeyPem = toPem(privateKey, "private");

      const publicKeyBlob = new Blob([publicKey], { type: "application/x-pem-file" });
      const privateKeyBlob = new Blob([privateKey], { type: "application/x-pem-file" });

      // const publicKeyUrl = URL.createObjectURL(publicKeyBlob);
      // const privateKeyUrl = URL.createObjectURL(privateKeyBlob);

      downloadFile(publicKeyBlob, `${userUID}.pub`);
      downloadFile(privateKeyBlob, `${userUID}`);
    } catch (err: any) {
      alert("Could not create and save new key pair: " + err.message);
    }
  };


  const handlePrivateKeyUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !userUID) {
      alert("User must be authorized and select a private key file.");
      return;
    }

    try {
      const privateKeyArrayBuffer = await file.arrayBuffer();
      console.log("privateKeyArrayBuffer: ", privateKeyArrayBuffer);
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
        console.log("userUID: ", userUID);
        await keyStore.savePrivateKey(privateKey, userUID);
        setHasPrivateKey(true); 
        alert("Private key imported and saved.");
      }
    } catch (err) {
      alert("Could not import private key: " );
    }
  };


  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      alert("No file selected.");
      return;
    }

    try {
      const currentPrivateKey = await keyStore?.getPrivateKeyByUserUID(userUID);
      console.log("currentPrivateKey: ", currentPrivateKey);
      if (!currentPrivateKey) {
        alert("No valid private key found.");
        return;
      }
      const reader = new FileReader();
      reader.onload = async function(event) {
        if (!event.target || !event.target.result) {
          alert("Error reading the file.");
          return;
        }
        const arrayBuffer = event.target.result;

        // Sign the image
        const signature = await window.crypto.subtle.sign(
          {
            name: "RSASSA-PKCS1-v1_5",
          },
          currentPrivateKey,
          arrayBuffer as BufferSource
        );

        // Handle the signed image data (e.g., upload to server)
        console.log("Image signed successfully:", new Uint8Array(signature));
        // You can now send the signature and image to your server
      };
      reader.readAsArrayBuffer(file);

    } catch (error) {
      console.error("Error signing the image:", error);
    }
  }


  // const createDataUrlFromByteArray = (byteArray: Uint8Array) => {
  //   let binaryString = '';
  //   for (let i = 0; i < byteArray.byteLength; i++) {
  //     binaryString += String.fromCharCode(byteArray[i]);
  //   }
  //   return "data:application/octet-stream;base64," + btoa(binaryString);
  // };

  return (
    <div>
      <h1>Key Management</h1>

      <section id="upload-image">
        <h1>Upload Image</h1>
        <input type="file" accept="image/*" disabled={!hasPrivateKey} onChange={handleImageUpload}/>
        {!hasPrivateKey && <p style={{ color: 'red' }}>You must upload a private key first.</p>}
      </section>

      <section id="create-keys">
        <h1>Create New Key Pair</h1>
        UserUID: <input type="text" value={userUID} onChange={(e) => setUserUID(e.target.value)} />
        <button onClick={handleCreateKeyPairClick}>Create Key Pair</button>
      </section>

      <section id="upload-private-key">
        <h1>Upload Private Key</h1>
        UserUID: <input type="text" value={userUID} onChange={(e) => setUserUID(e.target.value)} /><br />
        <input type="file" accept=".pem,.key" onChange={handlePrivateKeyUpload} />
      </section>

      {/* <section id="list-keys">
        <h1>Stored Keys</h1>
        <ul>
          {keys.map((key, index) => (
            <li key={index}>
              <a download={`${key.name}.publicKey`} href={key.spki}>{key.name}</a>
            </li>
          ))}
        </ul>
      </section> */}
    </div>
  );
};

export default KeyManagement;
