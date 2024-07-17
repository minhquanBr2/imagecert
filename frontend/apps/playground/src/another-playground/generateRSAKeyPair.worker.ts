import forge from 'node-forge';

self.onmessage = function() {
    const keyPair = forge.pki.rsa.generateKeyPair({ bits: 2048, e: 0x10001 });

    const publicKey = forge.pki.publicKeyToPem(keyPair.publicKey);
    const privateKey = forge.pki.privateKeyToPem(keyPair.privateKey);

    self.postMessage({ publicKey, privateKey });
    self.close();
};
