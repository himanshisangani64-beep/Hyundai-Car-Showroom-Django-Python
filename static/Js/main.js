// Preload images
const IMAGE_URLS = [
  "/static/images/photo/h.jpg",
  "/static/images/photo/b.jpg",
  "/static/images/photo/c.jpg",
  "/static/images/photo/n.jpg",
  "/static/images/photo/v.jpg",
  "/static/images/photo/aw.jpg"
];

IMAGE_URLS.forEach(url => {
  const img = new Image();
  img.src = url;
});

// Toggle dropdown
function toggleUserDropdown() {
  const dropdown = document.getElementById("userDropdown");
  dropdown.classList.toggle("show");
}

// Close dropdown if clicked outside
window.addEventListener("click", function(e) {
  const userIcon = document.querySelector(".user-icon");
  const dropdown = document.getElementById("userDropdown");

  if (!userIcon.contains(e.target)) {
    dropdown.classList.remove("show");
  }
});

// Keyboard support for user icon (Enter or Space)
document.addEventListener("keydown", function(e) {
  const userIcon = document.querySelector(".user-icon");
  if (
    (e.key === "Enter" || e.key === " ") &&
    document.activeElement === userIcon
  ) {
    e.preventDefault();
    toggleUserDropdown();
  }
});
