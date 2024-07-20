import '../styles/dropdown_modal_styles.css';

const Menu = ['Modify', 'Archive', 'Delete', 'Download', 'Properties'];

const DropdownModal = () => {
  return (
    <div className='dropdown_modal'>
      <div className='dropdown_container'>
        <ul className='options'>
          {Menu.map((menu) => (
            <li className='option' key={menu}>
              {menu}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default DropdownModal;
