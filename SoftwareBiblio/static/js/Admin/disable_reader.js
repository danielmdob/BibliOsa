var disableAdminBtn = document.getElementById("disableReaderBtn");
var disableAdminModal = document.getElementById("disableReaderModal");
var cancelDisableBtn = document.getElementById("cancelDisableBtn");

disableAdminBtn.onclick = function() {
    disableAdminModal.style.display = "block";
}

cancelDisableBtn.onclick = function() {
    disableAdminModal.style.display = "none";
}