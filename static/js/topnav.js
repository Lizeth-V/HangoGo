const burger = document.querySelector('.burger');
const navbarLinksLeft = document.querySelector('.navbar-links-left');
const navbarLinksRight = document.querySelector('.navbar-links-right');

burger.addEventListener('click', () => {
  navbarLinksLeft.classList.toggle('active');
  navbarLinksRight.classList.toggle('active');
});
