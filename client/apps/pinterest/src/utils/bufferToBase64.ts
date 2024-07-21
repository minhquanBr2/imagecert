export function arrayBufferToBase64(buffer: ArrayBuffer): string {
  if (!(buffer instanceof ArrayBuffer)) {
    throw new Error('Input is not an ArrayBuffer');
  }
  
  const bytes = new Uint8Array(buffer);
  console.log('bytes', bytes);

  const len = bytes.byteLength;
  if (len === 0) {
    console.error('ArrayBuffer is empty');
    return '';
  }

  let binary = '';
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }

  const result = btoa(binary);
  console.log('result', buffer, result);
  return result;
}
