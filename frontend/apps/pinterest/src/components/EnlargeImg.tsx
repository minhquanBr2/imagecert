import '../styles/enlarge_img_styles.css';

import React from 'react';

function handleClick(e: React.MouseEvent<HTMLImageElement, MouseEvent>, props : any){
  e.stopPropagation();
  props.setShowLargeImg(!props.showLargeImg);
}

const EnlargeImg = (props : any) => {
  return (
    <div className='background' style={{position: "fixed", height: "100%", width: "100%", top: 0, left: 0}}>
      <img onClick={(e) => handleClick(e, props)} className='image' src={props.src} alt='img' />
    </div>
  );
}

export default EnlargeImg;
