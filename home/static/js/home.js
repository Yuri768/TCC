const nav = document.querySelector(".nav-list");
const menuNav = document.querySelector(".Menu-navbar");

menuNav.addEventListener('click', function() {
    // Alternar classes active no menu hamburguer e no nav-list
    this.classList.toggle('active');
    nav.classList.toggle('active');
});
