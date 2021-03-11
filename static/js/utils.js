function openModal(el, id) {
    var modal = document.getElementById(id)
    if (id === "preview") {
        modal.getElementsByTagName("img")[0].src = el.src
        var button = modal.getElementsByTagName("a")[0]
        var url = button.href.split("/")
        url.splice(-2, 1, el.dataset.id)
        button.href = url.join("/")
    }

    modal.classList.add("is-active")
}

function closeModal(el) {
    el.closest(".modal").classList.remove("is-active")
}

function destroyModal(el) {
    el.closest(".modal").remove()
}

function displayUploadPreview(el) {
    document.getElementById("upload-preview").src = window.URL.createObjectURL(el.files[0])
}