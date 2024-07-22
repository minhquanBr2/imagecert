// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getFirestore } from '@firebase/firestore';
import { firebaseConfig } from './config';
import { getAuth } from 'firebase/auth';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const myConfig = firebaseConfig;

// Initialize Firebase
const app = initializeApp(myConfig);
export const firestore = getFirestore(app);
export const auth = getAuth(app);