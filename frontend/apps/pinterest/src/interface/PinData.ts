export interface PinData {
  author: string;
  board: string;
  description: string;
  pin_size: string;
  tags: string[];
  img_url: string;
}

export interface PinDetails extends PinData {
  imageId?: string;
  title: string;
}