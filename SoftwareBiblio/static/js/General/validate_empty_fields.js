var saveChangesBtn = document.getElementById("saveChangesBtn");
var fieldsAlert = document.getElementById("fieldsAlert");
var savedChangesDiv = document.getElementById("savedChangesDiv");
var fields = document.getElementsByClassName("mandatoryField");

saveChangesBtn.onclick = function() {
    if (areNotEmpty(fields)) {
        savedChangesDiv.style.display = "block";
        fieldsAlert.style.display = "none"
    } else {
        fieldsAlert.style.display = "block"
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