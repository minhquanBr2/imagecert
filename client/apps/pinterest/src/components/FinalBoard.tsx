import React, { useRef, useState, useContext, useEffect } from 'react';
import Popup from 'reactjs-popup';
import { deletePinBackend, fetchPinsBackend } from '../firebase_setup/DatabaseOperations.ts';
import { Tooltip } from 'antd';

import '../styles/final_board_styles.css';
import { Header, LoadingIcon, Modal, OpenPin, Pin } from './index.ts';
import RandomPin from './RandomPin.tsx';
import { PinDetails } from '../interface/PinData.ts';
import KeyStore from './KeyStore';
import KeyManager from './KeyManager';
import IndexedDBServices from '../service/indexDB';
import AuthContext from '../context/AuthContext';
import PopUpContent from './PopUpContent';
import "../styles/popup_content_styles.css";

import { Challenge } from '../service/caChallenge.ts';
import { getCertForPubkey } from '../service/signPublicKey.ts';
import { arrayBufferToBase64 } from '../utils/bufferToBase64.ts';
import { toast } from 'react-toastify';
import { ImageServices } from '../service/image.ts';

const FinalBoard: React.FC = () => {
  const animateRef = useRef(null);
  const [pinsFromDb, setPinsFromDb] = useState<any[]>([]);
  const [pinsToShow, setPinsToShow] = useState<any[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showOpenPin, setShowOpenPin] = useState(false);
  const [showGuidelines, setShowGuidelines] = useState(false);
  const [showLoading, setShowLoading] = useState(false);
  const [showGenerateKeyPopUp, setShowGenerateKeyPopUp] = useState(false);
  const [pinDetails, setPinDetails] = useState<PinDetails | null>(null);
  const { user } = useContext(AuthContext);
  const userUID = user?.uid as string;

  useEffect(() => {
    console.log("User UID: ", userUID);
    const checkForExistingPrivateKey = async () => {
      try {
        const existingPrivateKey = await IndexedDBServices.getItem("userPrivateKeyStore", userUID as string);
        if (existingPrivateKey) {
          setShowGenerateKeyPopUp(false); 
          console.log('Private key found in IndexedDB');
        }else {
          setShowGenerateKeyPopUp(true);
          console.log('No private key found in IndexedDB');
        }
      } catch (error) {
        console.error('Error checking for existing private key:', error);
      }
    };
    checkForExistingPrivateKey();
  }, [userUID]);  


  const handleGenerateNewKeyPair = async () => {
    try {
      const { publicKey, privateKey } = await KeyManager.generateKeyPair(userUID as string);
      await IndexedDBServices.setItem("userPrivateKeyStore", userUID as string, privateKey);
      await IndexedDBServices.setItem("userPublicKeyStore", userUID as string, publicKey);
      const result = await getCertForPubkey();
      console.log('Result: ', result);
      if (result){
        toast.success("Key pair uploaded successfully!");
        setShowGenerateKeyPopUp(false);
      }
      else {
        await IndexedDBServices.removeItem("userPrivateKeyStore", userUID as string);
        await IndexedDBServices.removeItem("userPublicKeyStore", userUID as string);
        toast.error("Key pair upload failed!");
      }

    } catch (error) {
      console.error('Error generating or storing new key pair:', error);
    }
  };


  const handleUploadKeyPair = async (event: any) => {
    const files = event.target.files;

    // Check if the user uploaded exactly 2 files
    if (files.length !== 2){
      alert("Please upload exactly 2 files: public key file (*.pub) and private key file (without extension).");
    }

    // Identify the files by their names
    let publicKeyFile: File | null = null;
    let privateKeyFile: File | null = null;
    for (let i = 0; i < files.length; i++) {
      if (files[i].name.endsWith('.pub')) {
        publicKeyFile = files[i];
      } else {
        privateKeyFile = files[i];
      }
    }
    console.log('Public key file: ', publicKeyFile);
    console.log('Private key file: ', privateKeyFile);

    // Ensure both public and private key files are identified
    if (!publicKeyFile || !privateKeyFile) {
      alert("Please upload a valid public key file (*.pub) and a private key file (without extension).");
      return;
    }

    // Process files
    try {
      const privateKey = await privateKeyFile.arrayBuffer();
      const privateKeyCryptoObject = await KeyManager.importPrivateKey(privateKey);
      await IndexedDBServices.setItem("userPrivateKeyStore", userUID as string, privateKey);         // only do this after ZKP challenge

      const publicKey = await publicKeyFile.arrayBuffer();
      const publicKeyCryptoObject = await KeyManager.importPublicKey(publicKey);
      await IndexedDBServices.setItem("userPublicKeyStore", userUID as string, publicKey);
      const result = await getCertForPubkey();
      console.log('Result: ', result);
      if (result){
        toast.success("Key pair uploaded successfully!");
        setShowGenerateKeyPopUp(false);
      }
      else {        
        await IndexedDBServices.removeItem("userPrivateKeyStore", userUID as string);
        await IndexedDBServices.removeItem("userPublicKeyStore", userUID as string);
        toast.error("Key pair upload failed: Old key pair detected!");
      }
    } catch (error) {
      console.error('Error uploading key pair:', error);
    }
  };


  const fetchPins = async () => {
    let pinsArray: any[] = [];
    const firebaseData = await ImageServices.getAll();
    console.log('Firebase data: ', firebaseData);
    firebaseData.map((pin: any) => {
      pinsArray.push(
        <Pin
          key={pin.imageID} 
          pinDetails={pin}
          openPin={openPin}
        />
      );
    });
    console.log("Pins array: ", pinsArray);
    setPinsFromDb(pinsArray);
    setPinsToShow(pinsArray);
  };

  useEffect(() => {
    fetchPins();
  }, []);

  const refreshPins = async () => {
    setShowModal(false);
    await fetchPins();
  };

  const openPin = (pinDetails: any) => {
    setPinDetails(pinDetails);
    setShowOpenPin(true);
  };

  const deletePin = async (pinDetails: any) => {
    await deletePinBackend(pinDetails);
    await fetchPins();
    setShowOpenPin(false);
  };

  const generateRandomPin = async (event: React.MouseEvent) => {
    setShowLoading(true);
    await RandomPin(event);
    await fetchPins();
    setShowLoading(false);
  };

  const filterPins = (filteredPins: any[]) => {
    setPinsToShow(filteredPins);
  };

  return (
    <div style={{ overflow: 'hidden', height: '100dvh', width: '100dvw' }} ref={animateRef}>  
      {/* <button onClick={() => getCertForPubkey("user_public_key")}>Challenge</button> */}
      <div>
        <Popup open={showGenerateKeyPopUp} closeOnDocumentClick={false}>
          <PopUpContent close={close} handleGenerateNewKeyPair={handleGenerateNewKeyPair} handleUploadKeyPair={handleUploadKeyPair}/>
        </Popup>
      </div>          
      <div className='header_container' id='header_bar'>
        <Header pinsToFilter={pinsFromDb} filterPins={filterPins} />
      </div>
      <div className='navigation_bar' id='navigation_bar'>
        <Tooltip title='Add new Pin'>
          <div onClick={() => setShowModal(true)} className='pint_mock_icon_container' id='add_pin'>
            <img src='./images/add.png' alt='add_pin' className='pint_mock_icon' />
          </div>
        </Tooltip>
      </div>
      <div className='pin_container' ref={animateRef} id='pin_container'>
        {pinsToShow}
      </div>
      <div 
        onClick={(event) => {
          const target = event.target as HTMLElement;
          if (target.className === 'add_pin_modal_container') {
            setShowModal(false);
          }
        }}
        className='add_pin_modal_container'
      >
        {showModal ? <Modal setShowModal={setShowModal} refreshPins={refreshPins} userUID={userUID as string}/> : null}
      </div>
      <div 
       onClick={(event) => {
        const target = event.target as HTMLElement;
        console.log('target: ', target);
        if (target.className === 'open_pin_modal_container') {
          setShowOpenPin(false);
        }
      }}
        className='open_pin_modal_container'
        >
        {showOpenPin ? <OpenPin setShowOpenPin={setShowOpenPin} pinDetails={pinDetails} deletePin={deletePin} /> : null}
      </div>
      {showLoading ? <LoadingIcon /> : null}
    </div>
  );
};

export default FinalBoard;
