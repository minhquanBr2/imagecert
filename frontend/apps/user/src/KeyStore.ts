


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
                    const objStore = this.db.createObjectStore(this.objectStoreName, { autoIncrement: true });
                    objStore.createIndex("name", "name", { unique: false });
                    objStore.createIndex("spki", "spki", { unique: false });
                }
            };
        });
    }

    saveKey(publicKey: CryptoKey, privateKey: CryptoKey | null, name: string): Promise<any> {
        return new Promise((fulfill, reject) => {
            if (!this.db) {
                return reject(new Error("KeyStore is not open."));
            }

            window.crypto.subtle.exportKey('spki', publicKey)
                .then((spki) => {
                    const savedObject = {
                        publicKey: publicKey,
                        privateKey: privateKey,
                        name: name,
                        spki: spki
                    };

                    const transaction = this.db!.transaction([this.objectStoreName], "readwrite");
                    transaction.onerror = (evt: any) => reject(evt.error);
                    transaction.onabort = (evt: any) => reject(evt.error);
                    transaction.oncomplete = () => fulfill(savedObject);

                    const objectStore = transaction.objectStore(this.objectStoreName);
                    objectStore.add(savedObject);
                })
                .catch((err) => reject(err));
        });
    }

    getKey(propertyName: "id" | "name" | "spki", propertyValue: any): Promise<any> {
        return new Promise((fulfill, reject) => {
            if (!this.db) {
                return reject(new Error("KeyStore is not open."));
            }

            const transaction = this.db.transaction([this.objectStoreName], "readonly");
            const objectStore = transaction.objectStore(this.objectStoreName);

            let request: IDBRequest;
            if (propertyName === "id") {
                request = objectStore.get(propertyValue);
            } else if (propertyName === "name") {
                request = objectStore.index("name").get(propertyValue);
            } else if (propertyName === "spki") {
                request = objectStore.index("spki").get(propertyValue);
            } else {
                return reject(new Error("No such property: " + propertyName));
            }

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
