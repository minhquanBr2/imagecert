import { GoogleAuthProvider, signInWithPopup, Auth } from "firebase/auth/web-extension";
import { addDoc } from "firebase/firestore";
import { auth, provider } from "../config";
import { database } from "../config";
import { child, get, getDatabase, ref, set } from "firebase/database";

const authorizeGoogle = () => {
  signInWithPopup(auth, provider)
  .then((result) => {
    // This gives you a Google Access Token. You can use it to access the Google API.
    const credential = GoogleAuthProvider.credentialFromResult(result);
    const token = credential?.accessToken;
    // The signed-in user info.
    const user = result.user;
    console.log(user);
    console.log(token);
    return {status: 1,user, token};
    // IdP data available using getAdditionalUserInfo(result)
    // ...
  }).catch((error) => {
    // Handle Errors here.
    const errorCode = error.code;
    const errorMessage = error.message;
    // The email of the user's account used.
    const email = error.customData.email;
    console.log(email);
    // The AuthCredential type that was used.
    const credential = GoogleAuthProvider.credentialFromError(error);
    // ...
    return {status: 0, errorCode, errorMessage, email, credential};
  });
}

const addNewUser = ({firebaseUID, publicKey, role} : {firebaseUID: string, publicKey: string, role: string}) => {
  // Add a new document with a generated id.
  set(ref(database, 'users/' + firebaseUID), {
    publicKey: publicKey,
    role: role
  }).then(() => {
    console.log("Document successfully written!");
    return 1;
  }).catch((error) => {
    console.error("Error writing document: ", error);
    return 0;
  });
}

const getUserOnce = (firebaseUID: string) => {
  const dbRef = ref(getDatabase());
  get(child(dbRef, `users/${firebaseUID}`)).then((snapshot) => {
    if (snapshot.exists()) {
      console.log(snapshot.val());
      return snapshot.val();
    } else {
      console.log("No data available");
      return null;
    }
  }).catch((error) => {
    console.error(error);
    return null;
  });
}


const UserServices = {
  authorizeGoogle,
  addNewUser,
  getUserOnce
}

export default UserServices;