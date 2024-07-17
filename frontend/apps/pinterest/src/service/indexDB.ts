import { openDB } from 'idb'
import { DB_NAME, DB_VERSION } from '../type/constant'

const getDB = async (storeName: string) => {
  return await openDB(DB_NAME, DB_VERSION, {
    upgrade(db : any) {
      if (!db.objectStoreNames.contains(storeName)) {
        db.createObjectStore(storeName)
      }
    },
  })
}

const setItem = async (storeName: string, key: string, value: any) => {
  const db = await getDB(storeName)
  const tx = db.transaction(storeName, 'readwrite')
  tx.objectStore(storeName).put(value, key)
  await tx.done
}

const getItem = async (storeName: string, key: string) => {
  const db = await getDB(storeName)
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
