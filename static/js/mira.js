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




