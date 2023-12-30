const likeButtons = document.querySelectorAll(".likeButton")
const postIDs = document.querySelectorAll(".postID")
let i = 0
let postIDValue = postIDs[i].value

likeButtons.forEach((likeButton) => {
	likeButton.addEventListener("click", (e) => {
		e.preventDefault()
		const xhr = new XMLHttpRequest()
		xhr.open("POST", `/post/${ postIDValue }/like`, true)
		xhr.onload = () => {
			if (xhr.status == 401) {
				alert(xhr.responseText)
			} else if (xhr.status == 200) {
				likeButton.innerHTML = `<span class="icon"><i class='bx bx-like is-size-4'></i>${xhr.responseText}</span>`
			}
		}
		xhr.send()
	})
	i+=1
})
