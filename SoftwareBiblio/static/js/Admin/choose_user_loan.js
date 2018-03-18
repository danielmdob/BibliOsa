var chooseUserBtn = document.getElementById("chooseUserBtn")
var userSelectionModal = document.getElementById("userSelectionModal");
var span = document.getElementById("userSelectionSpan");
var searchDiv = document.getElementById("searchDiv");
var originalStyle = searchDiv.style.display;
var readerNameBtn = document.getElementById("readerNameBtn");
var readerNameModal = document.getElementById("readerNameModal");
var cancelReaderNameBtn = document.getElementById("cancelReaderNameBtn");
var readerNameField = document.getElementById("readerNameField");

chooseUserBtn.onclick = function() {
    userSelectionModal.style.display = "block";
    searchDiv.style.display = "none";
}

span.onclick = function() {
    userSelectionModal.style.display = "none";
    searchDiv.style.display = originalStyle;
}

readerNameBtn.onclick = function() {
    readerNameModal.style.display = "block";
}

cancelReaderNameBtn.onclick = function() {
    readerNameModal.style.display = "none";
    readerNameField.value = "";
}