import '../styles/tags_creator_styles.css';

function TagsCreator(props : any){
  const removeTags = (indexToRemove : number) => {
    props.setTags([...props.tags.filter((_ : any, index : number) => index !== indexToRemove)]);
  };

  return (
    <div className='tags-container'>
      <div className='tags-input'>
        <ul id='tags'>
          {props.tags.map((tag : string, index: number) => (
            <li key={index} className='tag'>
              <span className='tag-title'>{tag}</span>
              {props.editable ? (
                <span className='tag-close-icon' onClick={() => removeTags(index)}>
                  🞬
                </span>
              ) : null}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default TagsCreator;
