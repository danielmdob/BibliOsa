var customDateBtn = document.getElementById("customDateBtn");
var customDateModal = document.getElementById("customDateModal");
var span = document.getElementsByClassName("close")[0];

customDateBtn.onclick = function() {
    customDateModal.style.display = "block";
}

span.onclick = function() {
    customDateModal.style.display = "none";
}