const likeButton = document.querySelector("#likeButton")
const postID = document.querySelector("#postID")

likeButton.addEventListener("click", (e) => {
	e.preventDefault()
	const xhr = new XMLHttpRequest()
	xhr.open("GET", `/post/${ postID.value }/like`, true)
	xhr.onload = () => {
		likeButton.innerText = `Likes: ${xhr.responseText}`
	}
	xhr.send()
})
