import React, { useEffect, useContext, useState } from 'react';
import TagsCreator from './TagsCreator'; // Adjust the import according to your file structure
import LoadingIcon from './LoadingIcon'; // Adjust the import according to your file structure
import { savePinBackend } from '../firebase_setup/DatabaseOperations';
import { PinData, PinDetails } from '../interface/PinData';
import { checkSize } from '../utils/checkSize';
import '../styles/modal_styles.css';
import { toast } from 'react-toastify';
import { ImageServices } from '../service/image';
import KeyManager from './KeyManager';
import { AUTH_KEY } from '../type/constant';
import { responsiveArray } from 'antd/es/_util/responsiveObserver';

let img_file : File;

function uploadImage(event: React.ChangeEvent<HTMLInputElement>, pinDetails: any, setPinDetails: React.Dispatch<React.SetStateAction<any>>, setShowLabel: React.Dispatch<React.SetStateAction<boolean>>, setShowModalPin: React.Dispatch<React.SetStateAction<boolean>>) {
  if (event.target.files && event.target.files[0]) {
    if (/image\/*/.test(event.target.files[0].type)) {
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = function () {
        setPinDetails({
          ...pinDetails,
          img_url: reader.result,
        });
        setShowLabel(false);
        setShowModalPin(true);
      };
      img_file = event.target.files[0];
    }
  }
}

async function savePin(
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>, 
  e: React.MouseEvent<HTMLDivElement>, 
  pinDetails: PinData, 
  refreshPins: () => void,
  userUID: string) {
  setIsLoading(true);
  
  const user = JSON.parse(sessionStorage.getItem(AUTH_KEY) as string);
  console.log('pinDetails', pinDetails, user);
  const pin_metadata : PinDetails = {
    ...pinDetails,
    author: user.uid,
    board: 'default',
    title: (document.querySelector('#pin_title') as HTMLInputElement).value,
    description: (document.querySelector('#pin_description') as HTMLInputElement).value,
    pin_size: (document.querySelector('#pin_size') as HTMLSelectElement).value,
    tags: pinDetails.tags,
  };

  console.log('pin_metadata', pin_metadata);
  const signature = await KeyManager.signImage(userUID, img_file);
  console.log('Signature:', signature);  
  ImageServices.uploadImage(img_file, signature).then((response) => {
    console.log(response);
    toast.success(response.message);
    refreshPins();
    setIsLoading(false);
  }).catch((error) => {
    console.error('Error uploading image', error);
    toast.error('Error uploading image');
    setIsLoading(false);
    return;
  });
}


const Modal: React.FC<ModalProps> = (props) => {
  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
    if (window.onscrollend !== undefined) {
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  const [pinDetails, setPinDetails] = useState<PinDetails>({
    author: '',
    board: '',
    description: '',
    img_url: '',
    pin_size: '',
    tags: ['Default', 'Pin'],
    title: '',
  });
  const [showLabel, setShowLabel] = useState(true);
  const [showModalPin, setShowModalPin] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [tags, setTags] = useState<string[]>(pinDetails.tags);

  const addTag = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.currentTarget.value !== '') {
      setTags([...tags, event.currentTarget.value]);
      setPinDetails({
        ...pinDetails,
        tags: [...tags, event.currentTarget.value],
      });
      event.currentTarget.value = '';
    }
  };

  const modalRef = React.useRef<HTMLDivElement>(null);

  const handleClickOutside = (event: any) => {
    if (modalRef.current && !modalRef.current.contains(event.target)) {
      props.setShowModal(false);
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className='add_pin_modal'>
      <div className='add_pin_container' ref={modalRef}>
        <div className='side' id='left_side'>
          <div className='section1'>
            <div className='pint_mock_icon_container'>
              <img src='./images/ellipse.png' alt='edit' className='pint_mock_icon' />
            </div>
          </div>
          <div className='section2'>
            <label htmlFor='upload_img' id='upload_img_label' style={{ display: showLabel ? 'block' : 'none' }}>
              <div className='upload_img_container' id='upload_img_container'>
                <div id='dotted_border'>
                  <div className='pint_mock_icon_container'>
                    <img src='./images/up-arrow.png' alt='upload_img' className='pint_mock_icon' />
                  </div>
                  <div>Click to upload</div>
                  <div>Recommendation: Use high-quality .jpg less than 20MB</div>
                </div>
              </div>
              <input
                onChange={(event) => uploadImage(event, pinDetails, setPinDetails, setShowLabel, setShowModalPin)}
                type='file'
                name='upload_img'
                id='upload_img'
                value=''
              />
            </label>
            <div className='modals_pin' style={{ display: showModalPin ? 'block' : 'none' }}>
              <div className='pin_image'>
                <img onLoad={checkSize} src={pinDetails.img_url} alt='pin_image' />
              </div>
            </div>
          </div>
          {/* <div className='section3'>
            <div className='save_from_site'>Save from site</div>
          </div> */}
        </div>
        <div className='side' id='right_side'>
          <div className='section1'>
            <div className='select_size' id='select_size'>
              <select defaultValue='medium' name='pin_size' id='pin_size'>
                <option value='small'>Small</option>
                <option value='medium'>Medium</option>
                <option value='large'>Large</option>
              </select>
              <div
                onClick={(e) => savePin(setIsLoading, e, pinDetails, props.refreshPins, props.userUID)}
                className='save_pin'
              >
                Save
              </div>
            </div>
          </div>
          <div className='section2' id='pin_details'>
            <input placeholder='Add your title' type='text' className='new_pin_input' id='pin_title' />
            <input placeholder='Describe what the Pin is about' type='text' className='new_pin_input' id='pin_description' />
            {/* <input placeholder='Add a location link' type='text' className='new_pin_input' id='pin_location' /> */}
            <input
              placeholder='Add tags by clicking Enter'
              type='text'
              className='new_pin_input'
              id='pin_tags'
              onKeyUp={(event) => (event.key === 'Enter' ? addTag(event) : null)}
            />
          </div>
          <div className='section3' id='tags_container'>
            <TagsCreator tags={tags} setTags={setTags} editable={true} />
          </div>
        </div>
      </div>
      {isLoading ? <LoadingIcon /> : null}
    </div>
  );
};

export default Modal;
