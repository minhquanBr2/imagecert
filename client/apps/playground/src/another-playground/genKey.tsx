import React from 'react';
import { useRSAKeyPair } from './useRSAKeyPair';

const App: React.FC = () => {
    const keys = useRSAKeyPair();

    return (
        <div>
            <h1>RSA Key Pair Generator</h1>
            {keys ? (
                <div>
                    <h2>Public Key:</h2>
                    <pre>{keys.publicKey}</pre>
                    <h2>Private Key:</h2>
                    <pre>{keys.privateKey}</pre>
                </div>
            ) : (
                <p>Generating keys...</p>
            )}
        </div>
    );
};

export default App;
