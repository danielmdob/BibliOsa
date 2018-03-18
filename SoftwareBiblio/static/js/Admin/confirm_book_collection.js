//Basado en: https://www.w3schools.com/howto/howto_css_modals.asp
// Get the modal
var brModal = document.getElementById('bookReturnModal');
var allBooksModal = document.getElementById('allBooksModal');

// Get the button that opens the modal
var bookBtn = document.getElementById("myBtn");
var allBooksBtn = document.getElementById("allBooksBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var spans = document.getElementsByClassName("close").length;
var allBooksSpan = document.getElementsByClassName("close")[spans - 1];

// When the user clicks on the button, open the modal 
bookBtn.onclick = function() {
    brModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    brModal.style.display = "none";
}

allBooksSpan.onclick = function() {
    allBooksModal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        brModal.style.display = "none";
    }
}

allBooksBtn.onclick = function() {
    allBooksModal.style.display = "block";
}