import { useState, useEffect } from 'react';

export function useRSAKeyPair() {
    const [keys, setKeys] = useState<{ publicKey: string; privateKey: string } | null>(null);

    useEffect(() => {
        const worker = new Worker(new URL('./generateRSAKeyPair.worker.ts', import.meta.url));
        
        worker.onmessage = (event) => {
            setKeys(event.data);
        };

        worker.postMessage(null);

        return () => {
            worker.terminate();
        };
    }, []);

    return keys;
}
