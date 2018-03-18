var agregar = document.getElementById('agregarLibro');

var ManualAdd = function () {

	var handleManualAdd = function () {

         $('.manual-add-form').validate({
	            errorElement: 'span', //default input error message container
	            errorClass: 'help-block', // default input error message class
	            focusInvalid: false, // do not focus the last invalid input
	            ignore: "",
	            rules: {
	                
	                title: {
	                    required: true
	                },
	                author: {
	                    required: true
	                },
	                serie: {
	                    required: true
	                },
	                year: {
	                    required: true
	                },
	                editorial: {
	                	required: true
	                },
	                isbn: {
	                    required: true
	                },
	                pages: {
	                    required: true
	                },
	                copies: {
	                    required: true
	                },
	                available: {
	                    required: true
	                },
	                onloan: {
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
	            },


	            submitHandler: function (form) {
	                form.submit();
	            }
	        });

			agregar.onclick = function (){
	                if ($('.manual-add-form').validate().form()) {
	                    $('.manual-add-form').submit();
	                } else {
	                document.getElementById('media-div').style.height = "1300px";
	            }
	                return false;
			}
	}
    
    return {
        //main function to initiate the module
        init: function () {
            handleManualAdd();    
        }
    };

}();

jQuery(document).ready(function() {
    ManualAdd.init();
});
