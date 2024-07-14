import React, { useRef, useState, useEffect } from 'react';
import { deletePinBackend, fetchPinsBackend } from '../firebase_setup/DatabaseOperations.ts';
import { Tooltip } from 'antd';

import '../styles/final_board_styles.css';
import autoAnimate from '@formkit/auto-animate';
import { Header, LoadingIcon, Modal, OpenPin, Pin } from './index.ts';
import RandomPin from './RandomPin.tsx';


const FinalBoard: React.FC = () => {
  const animateRef = useRef(null);

  const [pinsFromDb, setPinsFromDb] = useState<any[]>([]);
  const [pinsToShow, setPinsToShow] = useState<any[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showOpenPin, setShowOpenPin] = useState(false);
  const [showGuidelines, setShowGuidelines] = useState(false);
  const [showLoading, setShowLoading] = useState(false);
  const [pinDetails, setPinDetails] = useState(null);

  useEffect(() => {
    fetchPins();
    if (animateRef.current) {
      autoAnimate(animateRef.current);
    }
  }, []);

  const fetchPins = async () => {
    let pinsArray: any[] = [];
    // let fetchedPins: any[] = await fetchPinsBackend().catch((error) => console.error(error));
    let fetchedPins: any[] = [];
    fetchedPins.forEach((p) => {
      pinsArray.push(<Pin pinDetails={p} key={p.id} openPin={openPin} deletePin={deletePin} />);
    });
    setPinsFromDb(pinsArray);
    setPinsToShow(pinsArray);
  };

  const refreshPins = async () => {
    setShowModal(false);
    await fetchPins();
  };

  const openPin = (pinDetails: any) => {
    setPinDetails(pinDetails);
    setShowOpenPin(true);
  };

  const deletePin = async (pinDetails: any) => {
    // todo: add loading mode and/or transition state (blur the pin, fade it out etc)
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
      <div className='header_container' id='header_bar'>
        <Header pinsToFilter={pinsFromDb} filterPins={filterPins} />
      </div>
      <div className='navigation_bar' id='navigation_bar'>
        <Tooltip title='Add new Pin'>
          <div onClick={() => setShowModal(true)} className='pint_mock_icon_container' id='add_pin'>
            <img src='./images/add.png' alt='add_pin' className='pint_mock_icon' />
          </div>
        </Tooltip>
        {/* <Tooltip title='Generate random Pin'>
          <div onClick={(event) => generateRandomPin(event)} className='pint_mock_icon_container add_pin'>
            <img src='./images/shuffle.png' alt='random' className='pint_mock_icon' />
          </div>
        </Tooltip> */}
        {/* <Tooltip title='Refresh Pins'>
          <div onClick={() => refreshPins()} className='pint_mock_icon_container add_pin'>
            <img src='./images/refresh.png' alt='refresh' className='pint_mock_icon' />
          </div>
        </Tooltip>
        <Tooltip title='Show guidelines'>
          <div onClick={() => setShowGuidelines(true)} className='pint_mock_icon_container add_pin'>
            <img src='./images/help.png' alt='help' className='pint_mock_icon' />
          </div>
        </Tooltip> */}
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
        {showModal ? <Modal refreshPins={refreshPins} /> : null}
      </div>
      <div 
       onClick={(event) => {
        const target = event.target as HTMLElement;
        if (target.className === 'open_pin_modal_container') {
          setShowOpenPin(false);
        }
      }}
        className='open_pin_modal_container'
        >
        {showOpenPin ? <OpenPin pinDetails={pinDetails} deletePin={deletePin} /> : null}
      </div>
      {/* <div onClick={(event) => (event.target.className === 'guidelines_modal' ? setShowGuidelines(false) : null)} className='guidelines_modal_container'>
        {showGuidelines ? <Guidelines /> : null}
      </div> */}
      {showLoading ? <LoadingIcon /> : null}
    </div>
  );
};

export default FinalBoard;
