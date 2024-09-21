import React, { useRef, useEffect} from "react";

type ModalProps = {
  close: () => void;
  handleGenerateNewKeyPair: () => Promise<boolean>;
  handleUploadKeyPair: (event: any) => Promise<boolean>;
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
        <div>
          <button style={{ border: "2px solid #000", background:"white", padding:"5px 10px", margin: "0px 5px", fontSize: "14px"}} onClick={async () => await handleGenerateNewKeyPair()} > Generate new key pair </button>
        </div>    
        <div style={{position: "relative", display: "inline-block" }}>
            <input
              multiple
              id="filePicker"
              style={{ visibility: "hidden" }}
              type="file"
              onChange={async (event) => {
                await handleUploadKeyPair(event);
                (event.target as HTMLInputElement).value = "";                
              }}
            />
          <label htmlFor="filePicker" style={{ border: "2px solid #000", background:"white", padding:"5px 10px", margin: "0px 5px", fontSize: "14px", top: "50%", left: "50%", transform: "translate(-50%, -50%)", position: "absolute",  display: "flex", alignItems: "center", justifyContent: "center"}}> Upload private key file </label>
        </div>
      </div>  
    </div>
  );
};

export default PopUpContent;
