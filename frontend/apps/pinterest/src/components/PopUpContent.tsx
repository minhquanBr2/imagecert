import React, { useRef, useEffect} from "react";

type ModalProps = {
  close: () => void;
  handleGenerateNewKeyPair: () => void;
  handleUploadKeyPair: (event: any) => void;
};

const PopUpContent: React.FC<ModalProps> = ({ close, handleGenerateNewKeyPair, handleUploadKeyPair }) => {
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (contentRef.current && !contentRef.current.contains(event.target as Node)) {
        // Clicked outside the popup content
        event.stopPropagation();
      }
    };
    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  return (
    <div className="modal" ref={contentRef}>
      {/* <a className="close" onClick={close}>
        ×
      </a> */}
      <div className="header"> No private key found </div>
      <div className="content">
        In order to sign your image, you must provide a private key. You must either:
        <br></br> (1): Upload a private key file, which you stored on your local machine, or 
        <br></br> (2): Let us generate a key pair for you, which you should download and store on your local machine for future use. 
      </div>
      <div className="actions">       
        <button style={{ border: "2px solid #000", background:"white", padding:"5px 10px", margin: "0px 5px", fontSize: "14px"}} onClick={() => handleGenerateNewKeyPair()} > Generate new key pair </button>
        {/* <input type="file" id="file" name="file" onChange={(event) => handleUploadPrivateKey(event)} />
        <label htmlFor="file">Upload private key</label> */}
        <label htmlFor="filePicker" style={{ border: "2px solid #000", background:"white", padding:"5px 10px", margin: "0px 5px", fontSize: "14px" }}> Upload private key file </label>
        <input multiple id="filePicker" style={{visibility:"hidden"}} type={"file"} onChange={(event) => handleUploadKeyPair(event)}></input>
        {/* <button style="display:block;width:120px; height:30px;" onclick="document.getElementById('getFile').click()">Your text here</button>
        <input type='file' id="getFile" style="display:none"></input> */}
      </div>
    </div>
  );
};

export default PopUpContent;
