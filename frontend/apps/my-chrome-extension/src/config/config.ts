// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import { getDatabase } from 'firebase/database';

export const firebaseConfig = {
  apiKey: "AIzaSyAwxgE8l6N78tcCKV7RqCK8eWE86BGrL30",
  authDomain: "imageca-5c31b.firebaseapp.com",
  projectId: "imageca-5c31b",
  storageBucket: "imageca-5c31b.appspot.com",
  messagingSenderId: "59672534366",
  appId: "1:59672534366:web:056b17bfefc96fc11a43cf",
  measurementId: "G-C92JHBJ2FC",
  databaseUrl: "https://imageca-5c31b-default-rtdb.asia-southeast1.firebasedatabase.app/"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const database = getDatabase(app);
export const provider = new GoogleAuthProvider();
export const auth = getAuth();
auth.languageCode = 'it';

