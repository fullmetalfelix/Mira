

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




/* *** UPLOAD PAGE *** ****************************************************** */


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
			original: file.name,
			dataURL: event.target.result,
			tags: $('#tags').val().trim(),
			loc: $('#loc').val().trim(),
			mime: event.target.result.split(';base64,', 1)
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

	console.log('upload:'); console.log(mira_data);

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

/* ************************************************************************** */

/* *** SEARCH PAGE *** ****************************************************** */


function mira_search() {

	let request = {
		loc: $('#loc').val().trim(),
		tags: $('#tags').val().trim(),
	}

	$('.spinner').show();
	snackBar('searching...');
	$('button').prop('disabled', true);


	$.ajax({
		url: '/search/request',
		data: JSON.stringify(request),
		contentType: 'application/json;charset=UTF-8',
		type: 'POST',
		success: function(response) {

			response = JSON.parse(response);

			// show message and unlocks the UI
			$('.spinner').hide();
			$('button').prop('disabled', false);
			snackBar(response.message);

			if(response.type == 'success')
				mira_search_list(response.results);

		},
		error: function(error) {
			
			$('.spinner').hide();
			$('button').prop('disabled', false);
			snackBar('S3RVER ERR0R', {error: true}); console.log(error);
		}
	});
}

function mira_search_list(results) {

	let container = $('#results tbody');
	container.find('[data-img]').remove();

	let template = container.find('[data-template="img"]');

	results.forEach((o,i) => {

		let div = template.clone();
		div.removeAttr('data-template');
		div.attr('data-img', o._id['$oid']);
		div.show();

		div.find('#uptime').text(moment(o.uptime["$date"]).calendar(null, {sameElse: 'DD/MMM/YYYY'}));
		div.find('#filename').text(o.original);

		container.append(div);
	})

}



function mira_search_open(control) {

	let imgID = jQuery(control).closest('tr').attr('data-img');
	window.location.href = "/show/" + imgID;
}

/* ************************************************************************** */

/* *** IMAGE SHOW SYSTEM *** ************************************************ */

function mira_show_refresh() {

	$('.spinner').show();
	snackBar('refreshing...');

	$.getJSON('/show/'+imageID+'/refresh', { },
	
		function(response) {

			imagedata = response.image;
			mira_show();
		}
	);

}


function mira_show() {

	mira_show_resize();

	$('.spinner').hide();
}

function mira_show_resize() {

	let cdiv = document.getElementById('canvasdiv');
	let canvas = document.getElementById('canvas');
	let ctx = canvas.getContext('2d');

	let img = new Image;
	img.onload = () => { 

		let aspect = img.width / img.height;

		console.log(canvas.width + " " + canvas.height);
		console.log(img.width + " " + img.height);
		canvas.width = cdiv.clientWidth;
		canvas.height = canvas.width / aspect; //cdiv.clientHeight;
		ctx.drawImage(img, 
			0,0, img.width, img.height,
			0,0, canvas.width, canvas.height);

		// for crops
		imagedata.crops.forEach((c,i) => {

			let coords = JSON.parse(JSON.stringify(c.coords));
			coords[0] *= canvas.width;
			coords[2] *= canvas.width;
			coords[1] *= canvas.height;
			coords[3] *= canvas.height;

			coords[2] -= coords[0];
			coords[3] -= coords[1];


			ctx.beginPath();
			ctx.lineWidth = "2";
			ctx.strokeStyle = "red";
			ctx.rect(coords[0], coords[1], coords[2], coords[3]); 
			ctx.stroke();
		});



	};
	img.src = imagedata.file;
}


function mira_show_cropinfo(control, show) {


}



function mira_show_delete() {

	window.location.href = '/show/delete/' + imageID;
}


/* ************************************************************************** */





