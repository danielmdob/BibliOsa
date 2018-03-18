var saveChangesBtn = document.getElementById("saveChangesBtn");
var fieldsAlert = document.getElementById("fieldsAlert");
var savedChangesDiv = document.getElementById("savedChangesDiv");
var fields = document.getElementsByClassName("mandatoryField");
var emailField = document.getElementById("emailField");
var emailAlert = document.getElementById("emailAlert");

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

saveChangesBtn.onclick = function() {
    if (areNotEmpty(fields) && validateEmail(emailField.value)) {
        savedChangesDiv.style.display = "block";
        fieldsAlert.style.display = "none";
        emailAlert.style.display = "none"
    } else if (!areNotEmpty(fields) && validateEmail(emailField.value)) {
        fieldsAlert.style.display = "block";
        savedChangesDiv.style.display = "none";
        emailAlert.style.display = "none";
    } else if (areNotEmpty(fields) && !validateEmail(emailField.value)) {
        emailAlert.style.display = "block";
        fieldsAlert.style.display = "none";
        savedChangesDiv.style.display = "none";
    } else if (!areNotEmpty(fields) && !validateEmail(emailField.value)) {
        emailAlert.style.display = "block";
        fieldsAlert.style.display = "block";
        savedChangesDiv.style.display = "none";
    }
}

function areNotEmpty(fields) {
    for(var i = 0; i < fields.length; i++) {
        if(!isNotEmpty(fields[i].value)) {
            return false;
        }
    }
    return true;
}

function isNotEmpty(string) {
    if (string.trim().length > 0) {
        return true;
    } else {
        return false;
    }
}