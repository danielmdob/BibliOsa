var addBookModal = document.getElementById("addBookModal");
var addBookBtn = document.getElementById("addBookBtn");
var addBookSpan = document.getElementById("addBookSpan");
var searchDiv = document.getElementById("searchDiv");
var originalStyle = searchDiv.style.display;

addBookBtn.onclick = function() {
    addBookModal.style.display = "block";
    searchDiv.style.display = "none";
}

addBookSpan.onclick = function() {
    addBookModal.style.display = "none";
    searchDiv.style.display = originalStyle;
}