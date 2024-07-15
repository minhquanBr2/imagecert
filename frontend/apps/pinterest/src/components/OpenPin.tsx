import React, { useState, useEffect, useRef } from 'react';
import EnlargeImg from './EnlargeImg';
import '../styles/open_pin_styles.css';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import { MoreOutlined } from '@ant-design/icons';
import { Dropdown, Button, Space, Tooltip } from 'antd';
import TagsCreator from './TagsCreator';
import { checkSize } from '../utils/checkSize';

const deletePin = (pinDetails: any, deletePin: any) => {
  //todo export sweetAlert popups to external file
  const MySwal = withReactContent(Swal);
  MySwal.fire({
    title: 'Delete this pin?',
    icon: 'error',
    width: 300,
    showCancelButton: true,
    confirmButtonColor: '#2ca34c',
    cancelButtonColor: '#e6002390',
    confirmButtonText: 'Yes',
    cancelButtonText: 'No',
  }).then((result) => {
    if (result.isConfirmed) {
      const pin_data = {
        ...pinDetails,
      };
      deletePin(pin_data);
      MySwal.fire({
        title: 'Deleted!',
        icon: 'success',
        width: 300,
      });
    }
  });
};

const OpenPin: React.FC<any> = (props) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.body.style.overflow = 'hidden';
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.body.style.overflow = 'unset';
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleClickOutside = (event: any) => {
    if ((modalRef.current) && !(modalRef.current as HTMLElement).contains(event.target)) {
      props.setShowOpenPin(false);
      console.log('clicked outside');
    }
  };

  window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });

  const [showLargeImg, setShowLargeImg] = useState(false);
  const [isEditable, setIsEditable] = useState(false);

  const items = [
    {
      label: <span onClick={() => setIsEditable(!isEditable)}>Edit</span>,
      key: '0',
    },
    {
      label: <span>Properties</span>,
      key: '1',
    },
    {
      type: 'divider',
    },
    {
      label: <span onClick={() => deletePin(props.pinDetails, props.deletePin)}>Delete</span>,
      key: '3',
    },
  ];
  console.log('props Pin details: ', props);

  return (
    <div className='open_pin_modal'>
      {showLargeImg ? <EnlargeImg src={props.pinDetails.img_url} showLargeImg={showLargeImg} setShowLargeImg={setShowLargeImg} /> : null}
      <div className='open_pin_container' ref={modalRef}>
        <div className='side' id='left_side_open'>
          <div className='open_section'>
            <div className='open_modals_pin'>
              <Tooltip title='Click to enlarge image' placement='bottom'>
                <div className='open_pin_image' onClick={() => setShowLargeImg(!showLargeImg)}>
                  {showLargeImg ? null : <img onLoad={checkSize} src={props.pinDetails.img_url} alt='pin_image' />}
                </div>
              </Tooltip>
            </div>
          </div>
        </div>

        <div className='side' id='right_side_open'>
          <div className='options_icon_container' id='options_icon'>
            <Dropdown menu={{ items } as {items : any[]}} trigger={['click']}>
              <Space direction='vertical'>
                <Space wrap>
                  <Tooltip title='More'>
                    <Button type='default' shape='circle' icon={<MoreOutlined />} />
                  </Tooltip>
                </Space>
              </Space>
            </Dropdown>
          </div>
          <div className='open_section'>
            <div className='open_pin_title'>{props.pinDetails.title}</div>
            <div className='new_pin_input'>{props.pinDetails.description}</div>
            <TagsCreator tags={props.pinDetails.tags} editable={isEditable} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default OpenPin;
