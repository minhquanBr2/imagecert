import React, { useState } from 'react';
import { readPrivateKeyFile, encryptPrivateKey, storePrivateKey, retrievePrivateKey, decryptPrivateKey } from './useKey';

const App: React.FC = () => {
    const [privateKey, setPrivateKey] = useState<string | null>(null);

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const key = await readPrivateKeyFile(file);
            const passphrase = prompt("Enter a passphrase to encrypt your private key:") || "";
            const encryptedKey = encryptPrivateKey(key, passphrase);
            storePrivateKey(encryptedKey);
            setPrivateKey(key);
        }
    };

    const handleRetrieveKey = async () => {
        const passphrase = prompt("Enter your passphrase to decrypt your private key:") || "";
        const encryptedKey = await retrievePrivateKey();
        const key = decryptPrivateKey(encryptedKey, passphrase);
        setPrivateKey(key);
    };

    return (
        <div>
            <h1>Image Signing with RSA</h1>
            <input type="file" onChange={handleFileUpload} />
            <button onClick={handleRetrieveKey}>Retrieve Private Key</button>
            {privateKey && <pre>{privateKey}</pre>}
        </div>
    );
};

export default App;
