

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
	mira_data = null;

	reader.onerror = function() {
		snackBar('Unable to read ' + file.name);
	};

	reader.onload = function(event) {

		mira_data = {
			filename: file.name,
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
		type: 'POST'})
	.done(function(resp) {
		let response = JSON.parse(resp);
		snackBar(response.message, {error: response.type != 'success'});
		mira_data = null;
	})
	.fail(function(xhr){
		snackBar('ŚERVER ERR0R', {error: true}); 
		console.log(xhr);
	})
	.always(function(){
		$('.spinner').hide();
		$('button').prop('disabled', false);
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
	$('button').prop('disabled', true);
	snackBar('searching...');

	$.ajax({
		url: '/search/request',
		data: JSON.stringify(request),
		contentType: 'application/json;charset=UTF-8',
		type: 'POST'})
	.done(function(resp){
		
		let response = JSON.parse(resp);
		snackBar(response.message, {error: response.type != 'success'});

		if(response.type == 'success')
			mira_search_list(response.results);
	})
	.fail(function(xhr){
		snackBar('SERVER ERR0R', {error: true}); 
		console.log(xhr);
	})
	.always(function(){
		$('.spinner').hide();
		$('button').prop('disabled', false);
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
			console.log(response.type);
			snackBar(response.message);

			imagedata = response.image;
			mira_show();
			if(response.type == 'inprogress') {
				$('[scan-disable]').prop('disabled', true);
			}
			else {
				$('[scan-disable]').prop('disabled', false);
			}
		}
	);
}


function mira_show() {

	mira_show_resize();
	mira_show_listcrops();


	$('.spinner').hide();
}

function mira_show_resize(selectedcrop=null) {

	let cdiv = document.getElementById('canvasdiv');
	let canvas = document.getElementById('canvas');
	let ctx = canvas.getContext('2d');

	let img = new Image;
	img.onload = () => { 

		let aspect = img.width / img.height;

		//console.log(canvas.width + " " + canvas.height);
		//console.log(img.width + " " + img.height);
		canvas.width = cdiv.clientWidth;
		canvas.height = canvas.width / aspect; //cdiv.clientHeight;
		ctx.drawImage(img, 
			0,0, img.width, img.height,
			0,0, canvas.width, canvas.height);

		// for crops
		imagedata.crops.forEach((c,i) => {

			let coords = JSON.parse(JSON.stringify(c.coords));
			coords[0] *= canvas.height
			coords[1] *= canvas.width;
			coords[2] *= canvas.height;
			coords[3] *= canvas.width;

			coords[2] -= coords[0];
			coords[3] -= coords[1];


			ctx.beginPath();
			if(selectedcrop != null) {
				if(selectedcrop != i) {
					ctx.lineWidth = "2";
					ctx.strokeStyle = "red";
				}
				else {
					ctx.lineWidth = "4";
					ctx.strokeStyle = "green";
				}
			} else {
				ctx.lineWidth = "2";
				ctx.strokeStyle = "red";
			}
			
			ctx.rect(coords[1], coords[0], coords[3], coords[2]); 
			ctx.stroke();
		});
	};
	img.src = imagedata.file;
}

// constructs the list of crops in the table
function mira_show_listcrops() {

	let container = $('#croptable tbody');
	let template = container.find('[data-template="crop"]');
	container.find('[data-crop]').remove();

	// for crops
	imagedata.crops.forEach((c,i) => {

		let div = template.clone();
		div.removeAttr('data-template');
		div.attr('data-crop', c._id['$oid']);

		div.find('#ID').text(i);
		div.find('#detector').text(c.detector);
		div.find('#cls').text(c.animal);

		div.show();
		container.append(div);
	});
}


function mira_show_cropinfo(control, show) {

	let cropIndex = null;
	if(show == true)
		cropIndex = jQuery(control).closest('[data-crop]').find('#ID').text();

	mira_show_resize(cropIndex);
}



function mira_show_scan() {

	
	$('.spinner').show();
	snackBar('detecting beasts...');
	$('button').prop('disabled', true);


	$.getJSON('/show/'+imageID+'/megascan', function(response) {
		console.log('megadetect done');
	})
	.done(function(response) {
		
		snackBar(response.message);
		$('button').prop('disabled', false);

		if(response.type != 'error') {
			imagedata.crops = [];
			mira_show_listcrops();
			mira_show_resize();
			$('[scan-disable]').prop('disabled', true);
		}
	})
	.fail(function() {
		snackBar('SERVER ERROR!', {error: true});
		$('button').prop('disabled', false);
	})
	.always(function() {
		$('.spinner').hide();
		
	});
}






function mira_show_delete() {

	window.location.href = '/show/delete/' + imageID;
}


/* ************************************************************************** */





