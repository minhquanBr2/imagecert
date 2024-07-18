import React from "react";

type ModalProps = {
  close: () => void;
};

const Modal: React.FC<ModalProps> = ({ close }) => (
  <div className="modal">
    <a className="close" onClick={close}>
      ×
    </a>
    <div className="header"> Modal Title </div>
    <div className="content">
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Atque, a nostrum.
      Dolorem, repellat quidem ut, minima sint vel eveniet quibusdam voluptates
      delectus doloremque, explicabo tempore dicta adipisci fugit amet
      dignissimos?
      <br />
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Consequatur sit
      commodi beatae optio voluptatum sed eius cumque, delectus saepe
      repudiandae explicabo nemo nam libero ad, doloribus, voluptas rem alias.
      Vitae?
    </div>
  </div>
);

export default Modal;
