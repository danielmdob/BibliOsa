var disableAdminBtn = document.getElementById("disableAdminBtn");
var disableAdminModal = document.getElementById("disableAdminModal");
var cancelDisableBtn = document.getElementById("cancelDisableBtn");

disableAdminBtn.onclick = function() {
    disableAdminModal.style.display = "block";
}

cancelDisableBtn.onclick = function() {
    disableAdminModal.style.display = "none";
}