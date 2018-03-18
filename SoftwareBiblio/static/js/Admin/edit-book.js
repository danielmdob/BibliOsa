// Get the modal
var modal1 = document.getElementById('delete-modal');
var modal2 = document.getElementById('cover-modal');
var modal3 = document.getElementById('author-modal');
var modal4 = document.getElementById('serie-modal');
var modal5 = document.getElementById('comment-modal');

// Get the button that opens the modal
var btn1 = document.getElementById("delete-modal-opener");
var btn2 = document.getElementById("cover-modal-opener");
var btn3 = document.getElementById("author-modal-opener");
var btn4 = document.getElementById("serie-modal-opener");
var btn5 = document.getElementById("comment-modal-opener");

var accept1 = document.getElementById('delete-submit-modal');
var accept2 = document.getElementById('cover-submit-modal');
var accept3 = document.getElementById('author-submit-modal');
var accept4 = document.getElementById('serie-submit-modal');
var accept5 = document.getElementById('comment-submit-modal');

var cancel1 = document.getElementById('delete-cancel-modal');
var cancel2 = document.getElementById('cover-cancel-modal');
var cancel3 = document.getElementById('author-cancel-modal');
var cancel4 = document.getElementById('serie-cancel-modal');
var cancel5 = document.getElementById('comment-cancel-modal');

// When the user clicks on the button, open the modal 
btn1.onclick = function() {
    modal1.style.display = "block";
}
btn2.onclick = function() {
    modal2.style.display = "block";
}
btn3.onclick = function() {
    modal3.style.display = "block";
}
btn4.onclick = function() {
    modal4.style.display = "block";
}
btn5.onclick = function() {
    modal5.style.display = "block";
}

accept1.onclick = function() {
	alert("Libro eliminado");
	modal1.style.display = "none";
}
accept2.onclick = function() {
    alert("Image submited");
    /*var url_string = window.location.href;
    var url = new URL(url_string);
    var book_isbn = url.searchParams.get("book_isbn");
    alert(book_isbn);
    $.ajax({
        type: 'POST',
        url: 'image_form_upload',
        data: {
            'book_isbn': book_isbn
        },
        dataType: 'json',
        success: function (data) {
            json_response = data.response;
          alert(json_response)
        }
      }).done(function () {
            alert("Done");
            modal2.style.display = "none";
    });*/
}
accept3.onclick = function() {
    alert("Autor agregado");
    modal3.style.display = "none";
}
accept4.onclick = function() {
    alert("Serie agregada");
    modal4.style.display = "none";
}
accept5.onclick = function() {
    alert("Comentario eliminado");
    modal5.style.display = "none";
}

cancel1.onclick = function() {
    modal1.style.display = "none";
}
cancel2.onclick = function() {
    modal2.style.display = "none";
}
cancel3.onclick = function() {
    modal3.style.display = "none";
}
cancel4.onclick = function() {
    modal4.style.display = "none";
}
cancel5.onclick = function() {
    modal5.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal1) {
        modal1.style.display = "none";
    }
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
    if (event.target == modal3) {
        modal3.style.display = "none";
    }
    if (event.target == modal4) {
        modal4.style.display = "none";
    }
    if (event.target == modal5) {
        modal5.style.display = "none";
    }
}
