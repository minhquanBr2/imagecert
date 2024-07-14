import React, { useState, useEffect } from 'react';


import { savePinBackend } from '../firebase_setup/DatabaseOperations.ts';
import '../styles/modal_styles.css';
import TagsCreator from './TagsCreator.tsx';
import LoadingIcon from './LoadingIcon.tsx';

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

function checkSize(event: React.SyntheticEvent) {
  const image = event.target as HTMLImageElement;
  image.classList.add('pin_max_width');
  if (!image.parentElement) return;
  if (image.getBoundingClientRect().width < image.parentElement.getBoundingClientRect().width || image.getBoundingClientRect().height < image.parentElement.getBoundingClientRect().height) {
    image.classList.remove('pin_max_width');
    image.classList.add('pin_max_height');
  }
  image.style.opacity = '1';
}

async function savePin(setIsLoading: React.Dispatch<React.SetStateAction<boolean>>, e: React.MouseEvent<HTMLDivElement>, pinDetails: any, refreshPins: () => void) {
  setIsLoading(true);
  const users_data = {
    ...pinDetails,
    author: 'Patryk',
    board: 'default',
    title: (document.querySelector('#pin_title') as HTMLInputElement).value,
    description: (document.querySelector('#pin_description') as HTMLInputElement).value,
    destination: (document.querySelector('#pin_destination') as HTMLInputElement).value,
    pin_size: (document.querySelector('#pin_size') as HTMLSelectElement).value,
  };

  await savePinBackend(e, users_data, img_file);

  refreshPins();
  setIsLoading(false);
}

function Modal(props : any){
  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
    if (window.onscrollend !== undefined) {
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);
  const [pinDetails, setPinDetails] = useState<{
    author: string;
    board: string;
    title: string;
    destination: string;
    description: string;
    img_url: string;
    pin_size: string;
    tags: string[];
  }>({
    author: '',
    board: '',
    title: '',
    destination: '',
    description: '',
    img_url: '',
    pin_size: '',
    tags: [],
  });
  const [showLabel, setShowLabel] = useState(true);
  const [showModalPin, setShowModalPin] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [tags, setTags] = useState<string[]>(['Default', 'Pin']);
  const addTag = (event: any) => {
    if (event.target.value !== '') {
      setTags([...tags, event.target.value]);
      setPinDetails({
        ...pinDetails,
        tags: tags,
      });
      event.target.value = '';
    }
  };

  return (
    <div className='add_pin_modal'>
      <div className='add_pin_container'>
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
              <input onChange={(event) => uploadImage(event, pinDetails, setPinDetails, setShowLabel, setShowModalPin)} type='file' name='upload_img' id='upload_img' value='' />
            </label>
            <div className='modals_pin' style={{ display: showModalPin ? 'block' : 'none' }}>
              <div className='pin_image'>
                <img onLoad={checkSize} src={pinDetails.img_url} alt='pin_image' />
              </div>
            </div>
          </div>

          <div className='section3'>
            <div className='save_from_site'>Save from site</div>
          </div>
        </div>
        <div className='side' id='right_side'>
          <div className='section1'>
            <div className='select_size' id='select_size'>
              <select defaultValue='medium' name='pin_size' id='pin_size'>
                <option value='small'>Small</option>
                <option value='medium'>Medium</option>
                <option value='large'>Large</option>
              </select>
              <div onClick={(e) => savePin(setIsLoading, e, pinDetails, props.refreshPins)} className='save_pin'>
                Save
              </div>
            </div>
          </div>
          <div className='section2' id='pin_details'>
            <input placeholder='Add your title' type='text' className='new_pin_input' id='pin_title' />
            <input placeholder='Describe what the Pin is about' type='text' className='new_pin_input' id='pin_description' />
            <input placeholder='Add a destination link' type='text' className='new_pin_input' id='pin_destination' />
            <input placeholder='Add tags by clicking Enter' type='text' className='new_pin_input' id='pin_tags' onKeyUp={(event) => (event.key === 'Enter' ? addTag(event) : null)} />
          </div>
          <div className='section3' id='tags_container'>
            <TagsCreator tags={tags} setTags={setTags} editable={true} />
          </div>
        </div>
      </div>
      {isLoading ? <LoadingIcon /> : null}
      {/* <ReactJoyride
        continuous
        scrollToFirstStep
        disableScrolling={true}
        showProgress
        showSkipButton
        steps={ModalSteps as any}
        styles={{
          options: {
            primaryColor: '#ff0400',
            textColor: '#004a14',
            zIndex: 1000,
          },
        }}
      /> */}
    </div>
  );
}

export default Modal;