import CryptoJS from 'crypto-js';


export function readPrivateKeyFile(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            resolve(event.target?.result as string);
        };
        reader.onerror = reject;
        reader.readAsText(file);
    });
}


export function encryptPrivateKey(privateKey: string, passphrase: string): string {
    return CryptoJS.AES.encrypt(privateKey, passphrase).toString();
}


export function storePrivateKey(encryptedKey: string) {
    const dbRequest = indexedDB.open("MyDatabase", 1);
    dbRequest.onupgradeneeded = function(event) {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains("keys")) {
            db.createObjectStore("keys", { keyPath: "id" });
        }
    };
    dbRequest.onsuccess = function(event) {
        const db = (event.target as IDBOpenDBRequest).result;
        const transaction = db.transaction(["keys"], "readwrite");
        const store = transaction.objectStore("keys");
        store.put({ id: "privateKey", value: encryptedKey });
    };
}


export function retrievePrivateKey(): Promise<string> {
    return new Promise((resolve, reject) => {
        const dbRequest = indexedDB.open("MyDatabase", 1);
        dbRequest.onsuccess = function(event) {
            const db = (event.target as IDBOpenDBRequest).result;
            const transaction = db.transaction(["keys"], "readonly");
            const store = transaction.objectStore("keys");
            const getRequest = store.get("privateKey");
            getRequest.onsuccess = function() {
                resolve(getRequest.result.value);
            };
            getRequest.onerror = reject;
        };
        dbRequest.onerror = reject;
    });
}


export function decryptPrivateKey(encryptedKey: string, passphrase: string): string {
    const bytes = CryptoJS.AES.decrypt(encryptedKey, passphrase);
    return bytes.toString(CryptoJS.enc.Utf8);
}

