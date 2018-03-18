var Login = function () {

	var handleRegister = function () {
			document.getElementById('send-submit-btn').onclick = function () {
	                    submitData();
	        };
			//$("#fullname").on("change paste keyup", function() {alert($(this).val());});
	};

    return {
        //main function to initiate the module
        init: function () {
            handleRegister();
        }
    };

}();

function submitData(){
	//PASAR DATOS DE JS A DJANGO CON AJAX
    var email = document.getElementById('email').value;
    var json_response;
    $.ajax({
        url: 'admin_send_invite',
        data: {
            'email': email
        },
        dataType: 'json',
        success: function (data) {
            json_response = data;
            alert(json_response.response)
        }
      });
}

jQuery(document).ready(function() {
    Login.init();
});
