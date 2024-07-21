export const checkSize = (event: React.SyntheticEvent) => {
  const image = event.target as HTMLImageElement;
  image.classList.add('pin_max_width');
  if (!image.parentElement) return;
  if (image.getBoundingClientRect().width < image.parentElement.getBoundingClientRect().width || image.getBoundingClientRect().height < image.parentElement.getBoundingClientRect().height) {
    image.classList.remove('pin_max_width');
    image.classList.add('pin_max_height');
  }
  image.style.opacity = '1';
}