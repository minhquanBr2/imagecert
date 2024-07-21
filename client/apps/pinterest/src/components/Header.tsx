import React, { useContext } from 'react';
import '../styles/header_styles.css';
import { MoreOutlined } from '@ant-design/icons';
import { Dropdown, Button, Space, Tooltip } from 'antd';
import AuthContext from '../context/AuthContext';

const filterResults = (event: React.ChangeEvent<HTMLInputElement>, props: any) => {
  let filteredPins = props.pinsToFilter.filter((pin: any) => {
    let tags = JSON.stringify(pin.props.pinDetails.tags);
    return tags.toLowerCase().indexOf(event.target.value.toLowerCase()) > -1;
  });
  props.filterPins(filteredPins);
};

const Header = (props: any) => {
  const { logOut } = useContext(AuthContext);

  //todo: extract Dropdown definitions to separate file
  const items = [
    {
      label: <span>Profile</span>,
      key: '0',
    },
    {
      label: <span>Settings</span>,
      key: '1',
    },
    {
      label: <span>Sign out</span>,
      key: '2',
      onClick: () => logOut(),
    },
  ];

  //Get user avatar and username
  const { user } = useContext(AuthContext);

  return (
    <div className='pinterest'>
      <div className='left'>
        <Tooltip title='Homepage'>
          <a href='/' className='logo'>
            <img src='./images/fussek-logo-pinterest.png' alt='logo' className='logo' />
          </a>
        </Tooltip>
      </div>
      <div className='search'>
        <img src='./images/loupe.png' alt='loupe' style={{ maxHeight: '50%', paddingLeft: '15px', paddingRight: '10px', opacity: '0.5' }} />
        <input onChange={(event) => filterResults(event, props)} type='search' name='' placeholder='Search by keywords, f.ex. Nature or NYC' id='' />
      </div>
      <div className='right' style={{ width: "500px"}}>
        <div className='items'>
          <Dropdown menu={{ items }} trigger={['click']}>
            <Space direction='vertical'>
              <Space wrap>
                <Tooltip title='More'>
                  <Button type='default' shape='circle' icon={<MoreOutlined />} />
                </Tooltip>
              </Space>
            </Space>
          </Dropdown>
        </div>
        <Tooltip title='Profile'>
          <a href='/' className='avatar'>
            <div className='img' style={{ display: "flex", flexDirection: "row"}}>
              <img src={user?.photoURL} alt='' />
            </div>
          </a>
        </Tooltip>
        <div style={{ color: "black", fontSize: "16px", marginLeft: "20px"}} className='display-name'>{user?.displayName}</div>
      </div>
    </div>
  );
};

export default Header;
