
var modal2 = document.getElementById('cover-modal');
var modal3 = document.getElementById('author-modal');
var modal4 = document.getElementById('serie-modal');


var btn2 = document.getElementById("cover-modal-opener");
var btn3 = document.getElementById("author-modal-opener");
var btn4 = document.getElementById("serie-modal-opener");

var accept2 = document.getElementById('cover-submit-modal');
var accept3 = document.getElementById('author-submit-modal');
var accept4 = document.getElementById('serie-submit-modal');

var cancel2 = document.getElementById('cover-cancel-modal');
var cancel3 = document.getElementById('author-cancel-modal');
var cancel4 = document.getElementById('serie-cancel-modal');

// When the user clicks on the button, open the modal 
btn2.onclick = function() {
    modal2.style.display = "block";
}
btn3.onclick = function() {
    modal3.style.display = "block";
}
btn4.onclick = function() {
    modal4.style.display = "block";
}

accept2.onclick = function() {
    alert("Portada cambiada");
    modal2.style.display = "none";
}
accept3.onclick = function() {
    alert("Autor agregado");
    modal3.style.display = "none";
}
accept4.onclick = function() {
    alert("Serie agregada");
    modal4.style.display = "none";
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

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
    if (event.target == modal3) {
        modal3.style.display = "none";
    }
    if (event.target == modal4) {
        modal4.style.display = "none";
    }
}
