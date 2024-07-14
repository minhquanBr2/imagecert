import '../styles/enlarge_img_styles.css';

function handleClick(props : any){
  props.setShowLargeImg(!props.showLargeImg);
}

const EnlargeImg = (props : any) => {
  return (
    <div className='background'>
      <img onClick={() => handleClick(props)} className='image' src={props.src} alt='img' />
    </div>
  );
}

export default EnlargeImg;
