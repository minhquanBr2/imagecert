import { savePinBackend } from '../firebase_setup/DatabaseOperations.ts';
import { PinData } from '../interface/PinData.js';

const sizes = ['small', 'medium', 'large'];

const loremIpsum =
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae tempus orci. Nam nec dignissim neque. Ut eleifend, ex sed sodales facilisis, erat tortor accumsan urna, id rutrum mauris justo mollis leo. Ut tristique tempor augue a accumsan. Sed mollis quam vitae tellus porttitor, a ornare tortor aliquet. Sed venenatis felis at enim commodo, ac lacinia leo aliquet. Etiam nulla sem, ultricies eu eleifend ut, scelerisque lobortis massa. Sed eget luctus eros. Integer aliquet feugiat sem, ut lacinia leo. Sed porta facilisis orci semper ultrices. Proin vestibulum nisl eget urna fringilla, sed tincidunt nisl lacinia. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Duis ut condimentum dolor. Sed libero justo, dapibus id mauris quis, interdum fermentum dolor. Fusce varius metus non ipsum varius sagittis. Donec ullamcorper pulvinar leo et dapibus.';

export default async function RandomPin(event: React.MouseEvent) {
  event.preventDefault();

  const randomPin: PinData = {
    author: 'Patryk',
    board: 'default',
    title: 'Random Pin',
    description: loremIpsum,
    destination: 'http://metaphorpsum.com/',
    pin_size: sizes[Math.floor(Math.random() * sizes.length)],
    tags: ['Random', 'Generated', 'Pin', 'Example'],
  };

  //TODO: Implement image fetching from Unsplash API
  // try {
  //   const response = await fetch('https://source.unsplash.com/featured/1200x1600');
  //   const randomImg = await response.blob();
  //   await savePinBackend(event, randomPin, randomImg);
  // } catch (error) {
  //   console.error('Error generating random pin:', error);
  // }

  return randomPin;
}
