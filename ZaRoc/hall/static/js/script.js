const foreground = document.querySelector('.foreground');

const leftButton = document.querySelector('#left-button');

leftButton.onclick = function() {
  swapVisible();
  foreground.classList.remove('right');
  foreground.classList.add('left');
};

const rightButton = document.querySelector('#right-button');

rightButton.onclick = function() {
  swapVisible();
  foreground.classList.remove('left');
  foreground.classList.add('right');
};

const swapVisible = function() {
  const visible = document.querySelectorAll('.visible');
  const invisible = document.querySelectorAll('.invisible');

  Array.prototype.forEach.call(visible, e => e.classList.remove('visible'));
  Array.prototype.forEach.call(visible, e => e.classList.add('invisible'));
  Array.prototype.forEach.call(invisible, e => e.classList.remove('invisible'));
  Array.prototype.forEach.call(invisible, e => e.classList.add('visible'));
};