import imageCompression from 'browser-image-compression';
import { PinData, PinDetails } from '../interface/PinData.ts';
import { toast } from 'react-toastify';
import { getDatabase, set, ref, get, child } from 'firebase/database';

export async function fetchPinsBackend(): Promise<any[]> {
  let fetchedPins: any[] = [];
  const db = getDatabase();
  const dbRef = ref(db, 'pins/');
  const snapshot  = await get(dbRef);
  if (snapshot.exists()) {
    snapshot.forEach((childSnapshot) => {
      fetchedPins.push(childSnapshot.val());
    });
    //Sort fetch pin inverse order
    fetchedPins.sort((a, b) => (a.imageId > b.imageId) ? -1 : 1);
  } else {
    console.log('No data available');
  }
  
  return fetchedPins;
}

export async function savePinBackend(e: React.FormEvent, pins_metadata: PinDetails, imageFile: File): Promise<any> {
  try {
    const db = getDatabase();
    await set(ref(db, 'pins/' + pins_metadata.imageId), {
      author: pins_metadata.author,
      board: pins_metadata.board,
      description: pins_metadata.description,
      pin_size: pins_metadata.pin_size,
      tags: pins_metadata.tags,
      imageId: pins_metadata.imageId,
      img_url: pins_metadata.img_url,
      title: pins_metadata.title,
    });
    return 1;
  } catch (error) {
    console.error('Error adding document: ', error);
    return 0;
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
    toast.error('Error compressing image');
  }
  return compressedFile;
}

export async function deletePinBackend(pin_details: PinDetails): Promise<void> {
  // const storage = getStorage();
  // const pinRef = ref(storage, pin_details.id);

  // try {
  //   await deleteDoc(doc(firestore, 'pins', pin_details.id)).then(() => {
  //      deleteObject(pinRef)
  //     .then(() => {
  //       console.log('File deleted successfully');
  //     })
  //     .catch((e) => {
  //       console.log('Uh-oh, an error occurred!');
  //     });
  //   })

  // } catch (e) {
  //   console.error('Error deleting document: ', e);
  // }
}

export async function updatePinBackend(e: React.FormEvent, pins_metadata: PinData): Promise<void> {
  // Placeholder
}
