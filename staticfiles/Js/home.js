document.addEventListener("DOMContentLoaded", () => {
  const images = window.IMAGE_URLS || [];
  let idx = 0;
  const hero = document.querySelector('.hero-container');

  if (hero && images.length) {
    hero.style.backgroundImage = `url('${images[0]}')`;
    setInterval(() => {
      idx = (idx + 1) % images.length;
      hero.style.backgroundImage = `url('${images[idx]}')`;
    }, 5000);
  }

  const userIcon = document.querySelector(".user-icon");
  const dropdown = document.getElementById("userDropdown");

  if (userIcon && dropdown) {
    userIcon.addEventListener("click", event => {
      event.stopPropagation();
      dropdown.classList.toggle("active");
    });
    document.addEventListener("click", event => {
      if (!userIcon.contains(event.target)) {
        dropdown.classList.remove("active");
      }
    });
  }
});

  function toggleUserDropdown() {
    const dropdown = document.getElementById('userDropdown');
    const userIcon = document.querySelector('.user-icon');
    const isShown = dropdown.classList.toggle('show');
    userIcon.setAttribute('aria-expanded', isShown);
  }

  document.addEventListener('click', function (event) {
    const userIcon = document.querySelector('.user-icon');
    const dropdown = document.getElementById('userDropdown');
    if (!userIcon.contains(event.target)) {
      dropdown.classList.remove('show');
      userIcon.setAttribute('aria-expanded', false);
    }
  });
