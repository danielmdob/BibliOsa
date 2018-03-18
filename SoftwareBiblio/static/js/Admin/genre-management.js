// Get the modal
var modal1 = document.getElementById('delete-modal');
var modal2 = document.getElementById('edit-modal');
var modal3 = document.getElementById('add-modal');

var searchBar = document.getElementById('search-barr');

// Get the button that opens the modal
var btn1 = document.getElementById("delete-modal-opener");
var btn2 = document.getElementById("edit-modal-opener");
var btn3 = document.getElementById("add-modal-opener");

var accept1 = document.getElementById('delete-submit-modal');

var cancel1 = document.getElementById('delete-cancel-modal');

var accept2 = document.getElementById('edit-submit-modal');

var cancel2 = document.getElementById('edit-cancel-modal');

var accept3 = document.getElementById('add-submit-modal');

var cancel3 = document.getElementById('add-cancel-modal');

// When the user clicks on the button, open the modal 
btn1.onclick = function() {
    modal1.style.display = "block";
    searchBar.style.display = "none";
}

// When the user clicks on the button, open the modal 
btn2.onclick = function() {
    modal2.style.display = "block";
    searchBar.style.display = "none";
}
btn3.onclick = function() {
    modal3.style.display = "block";
    searchBar.style.display = "none";
}

accept1.onclick = function() {
	alert("Género eliminado");
	modal1.style.display = "none";
    searchBar.style.display = "block";
}

accept2.onclick = function() {
	alert("Género modificado");
	modal2.style.display = "none";
    searchBar.style.display = "block";
}
accept3.onclick = function() {
    alert("Género agregado");
    modal3.style.display = "none";
    searchBar.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
cancel1.onclick = function() {
    modal1.style.display = "none";
    searchBar.style.display = "block";
}

cancel2.onclick = function() {
    modal2.style.display = "none";
    searchBar.style.display = "block";
}
cancel3.onclick = function() {
    modal3.style.display = "none";
    searchBar.style.display = "block";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal1) {
        modal1.style.display = "none";
        searchBar.style.display = "block";
    }
    if (event.target == modal2) {
        modal2.style.display = "none";
        searchBar.style.display = "block";
    }
    if (event.target == modal3) {
        modal3.style.display = "none";
        searchBar.style.display = "block";
    }
}