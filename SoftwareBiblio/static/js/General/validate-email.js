var confirmBtn = document.getElementById("saveChangesBtn");
var emailField = document.getElementById("emailField");
var emailAlert = document.getElementById("emailAlert");

confirmBtn.onclick = function() {
    if (!validateEmail(emailField.value)) {
        emailAlert.style.display = "block";
    } else {
        emailAlert.style.display = "none";
    }
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}