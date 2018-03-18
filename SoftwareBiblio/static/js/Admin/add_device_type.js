var addTypeModal = document.getElementById("addTypeModal");
var addTypeBtn = document.getElementById("addTypeBtn");
var cancelAddTypeBtn = document.getElementById("cancelAddTypeBtn");
var typeNameField = document.getElementById("typeNameField");

addTypeBtn.onclick = function() {
    addTypeModal.style.display = "block";
}

cancelAddTypeBtn.onclick = function() {
    addTypeModal.style.display = "none";
    typeNameField.value = "";
}