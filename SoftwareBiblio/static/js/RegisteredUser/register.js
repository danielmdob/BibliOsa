var Login = function () {

	var handleRegister = function () {
         $('.register-form').validate({
	            errorElement: 'span', //default input error message container
	            errorClass: 'help-block', // default input error message class
	            focusInvalid: false, // do not focus the last invalid input
	            ignore: "",
	            rules: {

	                fullname: {
	                    required: true
	                },
                    cedula: {
	                    required: true
                    },
                    phone: {
	                    required: true
                    },
	                email: {
	                    required: true,
	                    email: true
	                },
	                address: {
	                    required: true
	                },
	                city: {
	                    required: true
	                },
	            },

	            invalidHandler: function (event, validator) { //display error alert on form submit

	            },

	            highlight: function (element) { // hightlight error inputs
	                $(element)
	                    .closest('.form-group').addClass('has-error'); // set error class to the control group
	            },

	            success: function (label) {
	                label.closest('.form-group').removeClass('has-error');
	                label.remove();
	                document.getElementById('boxcontent').style.height = '590px';
	            },

	            errorPlacement: function (error, element) {
	                if (element.attr("name") == "tnc") { // insert checkbox errors after the container
	                    error.insertAfter($('#register_tnc_error'));
	                    document.getElementById('boxcontent').style.height = '590px';
	                } else if (element.closest('.input-icon').size() === 1) {
	                    error.insertAfter(element.closest('.input-icon'));
	                    document.getElementById('boxcontent').style.height = '590px';
	                } else {
	                	error.insertAfter(element);
	                	document.getElementById('boxcontent').style.height = '590px';
	                }
	            },

	            submitHandler: function (form) {
	                form.submit();
	            }
	        });

			document.getElementById('register-submit-btn').onclick = function () {
	                if ($('.register-form').validate().form()) {
	                    submitData();
	                }
	                return false;
	        };

			//$("#fullname").on("change paste keyup", function() {alert($(this).val());});
	}

    return {
        //main function to initiate the module
        init: function () {
            handleRegister();
        }
    };

}();

function submitData(){
	//PASAR DATOS DE JS A DJANGO CON AJAX
    var fullname = document.getElementById("fullname").value;
    var cedula = document.getElementById('cedula').value;
    var email = document.getElementById('email').value;
    var address = document.getElementById('address').value;
    var city = document.getElementById('city').value;
    var phone = document.getElementById('phone').value;
    var json_response;
    $.ajax({
        url: 'finish_register',
        data: {
          'fullname': fullname,
            'cedula': cedula,
            'email': email,
            'address': address,
            'city': city,
            'phone': phone
        },
        dataType: 'json',
        success: function (data) {
            json_response = data;
          alert("Redireccionando...")
        }
      }).done(function () {
            if(json_response.dashboard == 0) {
                window.location.href = 'reader_dashboard';
            } else {
                window.location.href = 'admin_dashboard';
            }
    });
}

jQuery(document).ready(function() {
    Login.init();
});
