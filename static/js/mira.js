

/// Snackbar messages
var util_snackbars = [];
function snackBar(message, options={timeout: 3000, error: false}) {

	// Get the snackbar DIV
	var sbdiv = jQuery(document.createElement('div')); // jQuery(document.getElementById("snackbar"));
	sbdiv.attr('id', 'snackbar');
	sbdiv.addClass('show');
	if(options.error == true)
		sbdiv.css('color', 'red');

	sbdiv.text(message);
	sbdiv.css('z-index', 2000+util_snackbars.length);

	$('body').append(sbdiv);
	util_snackbars.push(sbdiv);
	
	let timeout = 3000;
	if(typeof options.timeout === 'number') timeout = options.timeout;


	// After 3 seconds, remove the show class from DIV
	setTimeout(function(){ 
		sbdiv.removeClass('show');
		setTimeout(function(){
			util_snackbars = util_snackbars.filter(o => o != sbdiv);
			sbdiv.remove();
		}, 1000);
	}, timeout);
}




var mira_data = null;
function mira_file_onchange() {

	let reader = new FileReader();
	let file = $('#file')[0].files[0];

	$('button').prop('disabled', true);

	reader.onerror = function() {
		snackBar('Unable to read ' + file.name);
	};

	reader.onload = function(event) {

		mira_data = {
			original: file.filename,
			dataURL: event.target.result,
			tags: $('#tags').val().trim(),
			loc: $('#loc').val().trim(),
			mime: event.target.result.split(';base64,', 1);
		};


		$('button').prop('disabled', false);
		snackBar('file ready');
	};
	reader.readAsDataURL(file);
}


function mira_upload() {

	$('.spinner').show();
	snackBar('uploading...');
	$('button').prop('disabled', true);

	$.ajax({
		url: '/upload/img',
		data: JSON.stringify(mira_data),
		contentType: 'application/json;charset=UTF-8',
		type: 'POST',
		success: function(response) {

			response = JSON.parse(response);

			// show message and unlocks the UI
			$('.spinner').hide();
			snackBar(response.message);
			mira_data = null;

		},
		error: function(error) {
			
			$('.spinner').hide();
			$('button').prop('disabled', false);
			snackBar('S3RVER ERR0R', {error: true}); console.log(error);
		}
	});

}



