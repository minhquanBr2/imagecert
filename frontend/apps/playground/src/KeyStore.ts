// async function generateAndExportKeyPair(): Promise<{ publicKeyFile: Blob, privateKeyFile: Blob }> {
//     const keyPair = await window.crypto.subtle.generateKey(
//         {
//             name: "RSASSA-PKCS1-v1_5",
//             modulusLength: 2048,
//             publicExponent: new Uint8Array([1, 0, 1]),
//             hash: "SHA-256"
//         },
//         true,
//         ["sign", "verify"]
//     );

//     const publicKey = await window.crypto.subtle.exportKey("spki", keyPair.publicKey);
//     const privateKey = await window.crypto.subtle.exportKey("pkcs8", keyPair.privateKey);

//     const publicKeyFile = new Blob([publicKey], { type: "application/x-pem-file" });
//     const privateKeyFile = new Blob([privateKey], { type: "application/x-pem-file" });

//     return { publicKeyFile, privateKeyFile };
// }


// async function importPrivateKey(privateKeyFile: Blob): Promise<CryptoKey> {
//     const privateKeyArrayBuffer = await privateKeyFile.arrayBuffer();
//     const privateKey = await window.crypto.subtle.importKey(
//         "pkcs8",
//         privateKeyArrayBuffer,
//         {
//             name: "RSASSA-PKCS1-v1_5",
//             hash: "SHA-256"
//         },
//         true,
//         ["sign"]
//     );
//     return privateKey;
// }




class KeyStore {
    private db: IDBDatabase | null = null;
    private readonly dbName = "KeyStore";
    private readonly objectStoreName = "keys";

    open(): Promise<this> {
        return new Promise((fulfill, reject) => {
            if (!window.indexedDB) {
                return reject(new Error("IndexedDB is not supported by this browser."));
            }

            const req = indexedDB.open(this.dbName, 1);

            req.onsuccess = (evt: any) => {
                this.db = evt.target.result;
                fulfill(this);
            };

            req.onerror = (evt: any) => {
                reject(evt.error);
            };

            req.onblocked = () => {
                reject(new Error("Database already open"));
            };

            req.onupgradeneeded = (evt: any) => {
                this.db = evt.target.result;
                if (this.db && !this.db.objectStoreNames.contains(this.objectStoreName)) {
                    const objStore = this.db.createObjectStore(this.objectStoreName, { keyPath: "id", autoIncrement: true });
                    objStore.createIndex("userUID", "userUID", { unique: false });
                }
            };
        });
    }


    savePrivateKey(privateKey: CryptoKey, userUID: string): Promise<any> {
        return new Promise((fulfill, reject) => {
            if (!this.db) {
                return reject(new Error("KeyStore is not open."));
            }

            const savedObject = {
                privateKey: privateKey,
                userUID: userUID
            };


            const transaction = this.db.transaction([this.objectStoreName], "readwrite");
            transaction.onerror = (evt: any) => reject(evt.error);
            transaction.onabort = (evt: any) => reject(evt.error);
            transaction.oncomplete = () => fulfill(savedObject);

            const objectStore = transaction.objectStore(this.objectStoreName);
            objectStore.add(savedObject);
        });
    }


    getPrivateKeyByUserUID(userUID: string): Promise<any> {
        return new Promise((fulfill, reject) => {
            if (!this.db) {
                return reject(new Error("KeyStore is not open."));
            }

            const transaction = this.db.transaction([this.objectStoreName], "readonly");
            const objectStore = transaction.objectStore(this.objectStoreName);
            const request = objectStore.index("userUID").get(userUID);

            request.onsuccess = (evt: any) => fulfill(evt.target.result);
            request.onerror = (evt: any) => reject(evt.target.error);
        });
    }


    listKeys(): Promise<any[]> {
        return new Promise((fulfill, reject) => {
            if (!this.db) {
                return reject(new Error("KeyStore is not open."));
            }

            const list: any[] = [];
            const transaction = this.db.transaction([this.objectStoreName], "readonly");
            transaction.onerror = (evt: any) => reject(evt.error);
            transaction.onabort = (evt: any) => reject(evt.error);

            const objectStore = transaction.objectStore(this.objectStoreName);
            const cursor = objectStore.openCursor();

            cursor.onsuccess = (evt: any) => {
                if (evt.target.result) {
                    list.push({ id: evt.target.result.key, value: evt.target.result.value });
                    evt.target.result.continue();
                } else {
                    fulfill(list);
                }
            };
        });
    }

    close(): Promise<void> {
        return new Promise((fulfill, reject) => {
            if (!this.db) {
                return reject(new Error("KeyStore is not open."));
            }

            this.db.close();
            this.db = null;
            fulfill();
        });
    }
}

export default KeyStore;
