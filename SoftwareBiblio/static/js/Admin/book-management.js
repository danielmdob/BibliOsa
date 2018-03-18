// Get the modal
var modal = document.getElementById('smart-add-modal');
var modal2 = document.getElementById('delete-modal');

// Get the button that opens the modal
var btn = document.getElementById("modal-opener");
var btn2 = document.getElementById("delete-modal-opener");

var accept = document.getElementById('submit-modal');
var accept2 = document.getElementById('delete-submit-modal');

var cancel = document.getElementById('cancel-modal');
var cancel2 = document.getElementById('delete-cancel-modal');

// When the user clicks on the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on the button, open the modal 
btn2.onclick = function() {
    modal2.style.display = "block";
}


accept.onclick = function() {
    var isbn = document.getElementById("isbnField").value;
         $.ajax({
        url: '/smart_add',
        data: {
          'isbn': isbn
        },
        dataType: 'json',
        success: function (data) {
          if (data.is_valid) {
              if (!data.already_added) {
                  alert("Se agregó exitosamente el libro con los siguiente datos:\n" + "Título: " + data.title + "\nEditorial: " + data.publisher + "\nISBN: " + data.isbn);
              } else {
                  alert("El libro ya se encuentra en el sistema, cambiar la cantidad de unidades en Editar Libro")
              }
          } else {
              alert("El ISBN ingresado no es válido o no se encontró suficiente información sobre el libro")
          }
        }
         });
        document.getElementById("isbnField").value = "";
	    modal.style.display = "none";
}

accept2.onclick = function() {
	alert("Libro eliminado");
	modal2.style.display = "none";
}
// When the user clicks on <span> (x), close the modal
cancel.onclick = function() {
    modal.style.display = "none";
}

cancel2.onclick = function() {
    modal2.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

window.onclick = function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
}