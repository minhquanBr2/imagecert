interface ModalProps {
  refreshPins: () => void;
  setShowModal: React.Dispatch<React.SetStateAction<boolean>>;
  userUID: string;
}