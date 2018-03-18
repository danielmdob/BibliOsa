// Get the modal
var modal1 = document.getElementById('book-modal');
var modal2 = document.getElementById('comment-modal');

// Get the button that opens the modal
var btn1 = document.getElementById("modal-opener-book");
var btn2 = document.getElementById("modal-opener-comment");
var btn3 = document.getElementById("edit_book_button");

var accept1 = document.getElementById('submit-modal-book');

var cancel1 = document.getElementById('cancel-modal-book');

var accept2 = document.getElementById('submit-modal-comment');

var cancel2 = document.getElementById('cancel-modal-comment');

// When the user clicks on the button, open the modal 
btn1.onclick = function() {
    modal1.style.display = "block";
}

// When the user clicks on the button, open the modal 
btn2.onclick = function() {
    modal2.style.display = "block";
}

btn3.onclick = function() {
    var url_string = window.location.href;
    var url = new URL(url_string);
    var book_isbn = url.searchParams.get("book_isbn");
    window.location.href = 'admin_edit_book?book_isbn='+book_isbn;
}


accept1.onclick = function() {
	alert("Libro eliminado");
	modal1.style.display = "none";
}

accept2.onclick = function() {
	alert("Comentario eliminado");
	modal2.style.display = "none";
}
// When the user clicks on <span> (x), close the modal
cancel1.onclick = function() {
    modal1.style.display = "none";
}

cancel2.onclick = function() {
    modal2.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal1) {
        modal1.style.display = "none";
    }
}

window.onclick = function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
}