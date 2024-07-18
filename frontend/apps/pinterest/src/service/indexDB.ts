import { openDB } from 'idb'
import { DB_NAME, DB_VERSION } from '../type/constant'

const openDatabase = async () => {
  return await openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      console.log('Upgrading database...');
      if (!db.objectStoreNames.contains('userPrivateKeyStore')) {
        db.createObjectStore('userPrivateKeyStore');
      }
      if (!db.objectStoreNames.contains('userPublicKeyStore')) {
        db.createObjectStore('userPublicKeyStore');
      }
    },
  });
};

const getDB = async (storeName: string) => {
  const db = await openDatabase();
  
  // Check if the store exists
  if (!db.objectStoreNames.contains(storeName)) {
    // Close the current db connection
    db.close();
    
    // Re-open the database with incremented version to create the new store
    const newVersion = db.version + 1;
    const newDb = await openDB(DB_NAME, newVersion, {
      upgrade(upgradeDb) {
        if (!upgradeDb.objectStoreNames.contains(storeName)) {
          console.log('Creating object store:', storeName);
          upgradeDb.createObjectStore(storeName);
        }
      },
    });
    
    return newDb;
  }
  
  return db;
};

const setItem = async (storeName: string, key: string, value: any) => {
  const db = await getDB(storeName)
  if (!db.objectStoreNames.contains(storeName)) {
    console.error('Object store not found:', storeName)
    return null
  }
  const tx = db.transaction(storeName, 'readwrite')
  tx.objectStore(storeName).put(value, key)
  await tx.done
}

const getItem = async (storeName: string, key: string) => {
  const db = await getDB(storeName)
  if (!db.objectStoreNames.contains(storeName)) {
    console.error('Object store not found:', storeName)
    return null
  }
  const tx = db.transaction(storeName, 'readonly')
  const value = await tx.objectStore(storeName).get(key)
  await tx.done
  return value
}

const removeItem = async (storeName: string, key: string) => {
  const db = await getDB(storeName)
  const tx = db.transaction(storeName, 'readwrite')
  tx.objectStore(storeName).delete(key)
  await tx.done
}

const IndexedDBServices = {
  setItem,
  getItem,
  removeItem,
}

export default IndexedDBServices
