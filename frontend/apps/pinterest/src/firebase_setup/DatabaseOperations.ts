import { collection, doc, addDoc, getDoc, updateDoc, getDocs, deleteDoc } from 'firebase/firestore';
import { getStorage, ref, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage';
import { firestore } from './firebase.ts';
import imageCompression from 'browser-image-compression';
import { PinData } from '../interface/PinData.ts';

interface PinDetails {
  id: string;
  // Add other fields as required
}

export async function fetchPinsBackend(): Promise<any[]> {
  let fetchedPins: any[] = [];
  try {
    await getDocs(collection(firestore, 'pins')).then((querySnapshot) => {
      const newData = querySnapshot.docs.map((doc) => ({ ...doc.data(), id: doc.id }));
      newData.forEach((p) => {
        fetchedPins.push(p);
      });
    });
  } catch (error) {
    console.log(error);
  }
  return fetchedPins;
}

export async function savePinBackend(e: React.FormEvent, users_data: PinData, imageFile: File): Promise<any> {
  let doc_snap;
  e.preventDefault();
  try {
    const docRef = await addDoc(collection(firestore, 'pins'), {
      ...users_data,
      img_url: '',
    });
    const storage = getStorage();
    const storageRef = ref(storage, docRef.id);
    let compressedImg = await compressImage(imageFile);
    if (!compressedImg) {
      return;
    }
    await uploadBytes(storageRef, compressedImg)
      .then((snapshot) => {
        console.log('Uploaded image for pin: ' + docRef.id);
        getDownloadURL(snapshot.ref)
          .then((url) => {
            updateDoc(docRef, { img_url: url })
              .then(() => {
                console.log('Update of pin successful!');
              })
              .catch((error) => {
                console.log(error);
              });
          })
          .catch((error) => {
            console.log(error);
          });
      })
      .catch((error) => {
        console.log(error);
      });
    doc_snap = await getDoc(docRef);
    return doc_snap.data();
  } catch (e) {
    console.error('Error adding document: ', e);
  }
}

async function compressImage(imageFile: File): Promise<File | undefined> {
  let compressedFile;
  const options = {
    maxSizeMB: 1,
  };
  try {
    compressedFile = await imageCompression(imageFile, options);
  } catch (error) {
    console.log(error);
  }
  return compressedFile;
}

export async function deletePinBackend(pin_details: PinDetails): Promise<void> {
  const storage = getStorage();
  const pinRef = ref(storage, pin_details.id);

  try {
    await deleteDoc(doc(firestore, 'pins', pin_details.id)).then(() => {
       deleteObject(pinRef)
      .then(() => {
        console.log('File deleted successfully');
      })
      .catch((e) => {
        console.log('Uh-oh, an error occurred!');
      });
    })

  } catch (e) {
    console.error('Error deleting document: ', e);
  }
}

export async function updatePinBackend(e: React.FormEvent, users_data: PinData): Promise<void> {
  // Placeholder
}
