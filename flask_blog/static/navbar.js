const navBarMenu = document.querySelector("#navBarMenu")
const navBarBurger = document.querySelector("#navBarBurger")

navBarBurger.addEventListener("click", () => {
	navBarMenu.classList.toggle("is-active")
})