const likeButton = document.querySelector("#likeButton")
const postID = document.querySelector("#postID")

likeButton.addEventListener("click", (e) => {
	e.preventDefault()
	const xhr = new XMLHttpRequest()
	xhr.open("POST", `/post/${ postID.value }/like`, true)
	xhr.onload = () => {
		if (xhr.status == 401) {
			alert(xhr.responseText)
		} else if (xhr.status == 200) {
			likeButton.innerText = `Likes: ${xhr.responseText}`
		}
	}
	xhr.send()
})

