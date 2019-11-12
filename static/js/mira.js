

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


var all = function(array){
    var deferred = $.Deferred();
    var fulfilled = 0, length = array.length;
    var results = [];

    if (length === 0) {
        deferred.resolve(results);
    } else {
        array.forEach(function(promise, i){
            $.when(promise()).then(function(value) {
                results[i] = value;
                fulfilled++;
                if(fulfilled === length){
                    deferred.resolve(results);
                }
            });
        });
    }

    return deferred.promise();
};



/* *** UPLOAD PAGE *** ****************************************************** */


var mira_data = null;
var mira_scroll_index = 0;

function mira_file_onchange() {

	let reader = new FileReader();
	let input = $('#file')[0];
	let file = $('#file')[0].files[0];
	
	mira_scroll_index = $('#file')[0].files.length-1;
	mira_upload_preview();
}

function mira_upload() {
	/*
	$('.spinner').show();
	snackBar('uploading...');
	$('#btOK').prop('disabled', true);

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
		//$('button').prop('disabled', true);
	});
	*/
}

function mira_upload_many() {

	let input = $('#file')[0];
	let files = Array.from(input.files);

	if(files.length == 0) {
		snackBar('No file selected!', {error: true});
		return;
	}

	$('.spinner').show();
	snackBar('uploading...');
	$('#btOK').prop('disabled', true);
	$('#file').prop('disabled', true);

	
	let promises = [];

	files.forEach((file) => {

		promises.push(function() {

			return $.Deferred(function(dfd) {

				let reader = new FileReader();
				reader.onerror = function() {
					snackBar('Unable to read ' + file.name);
					dfd.reject();
				};
				reader.onload = function(event) {
					let clientdata = {
						filename: file.name,
						dataURL: event.target.result,
						tags: $('#tags').val().trim(),
						loc: $('#loc').val().trim(),
						mime: event.target.result.split(';base64,', 1)
					};

					$.ajax({
						url: '/upload/img',
						data: JSON.stringify(clientdata),
						contentType: 'application/json;charset=UTF-8',
						type: 'POST'
					})
					.done(function(resp) {
						
					})
					.fail(function(xhr){
						snackBar('ŚERVER ERR0R', {error: true}); 
						console.log(xhr);
					})
					.always(function(){
						dfd.resolve();
					});

				};
				reader.readAsDataURL(file);
			}).promise();
		});
	}); // end of loop over images

	$.when(all(promises)).then(function() {
	    $('.spinner').hide();
	    snackBar('images were uploaded');
	    $('#btOK').prop('disabled', false);
	    $('#file').prop('disabled', false);
	});
}

function mira_upload_scroll(dir) {

	let input = $('#file')[0];
	let files = input.files;
	console.log(files);

	mira_scroll_index += dir;
	if(mira_scroll_index < 0) mira_scroll_index = files.length - 1;
	else if(mira_scroll_index == files.length) mira_scroll_index = 0;

	// update preview
	mira_upload_preview();
}

function mira_upload_preview() {

	let reader = new FileReader();
	let input = $('#file')[0];
	let file = input.files[mira_scroll_index];

	reader.onerror = function() {
		snackBar('Unable to read ' + file.name);
		$('#preview').attr('src', null);
		$('#prevfile').text('preview: ' + file.name + ' [invalid]');
	};

	reader.onload = function(event) {
		$('#prevfile').text('preview: ' + file.name);
		$('#preview').show();
		$('#preview').attr('src', event.target.result);
	};
	reader.readAsDataURL(file);

}


/* ************************************************************************** */
/* *** SEARCH PAGE *** ****************************************************** */


const img_status = {
	'-20': 'classifier - empty',
	'-10': 'detector - empty',
	'0': 'not processed',
	'1': 'scan in progress',
	'10': 'detector done',
	'20': 'classifier done',
};
var mira_search_results;


function mira_search() {

	let request = {
		loc: $('#loc').val().trim(),
		tags: $('#tags').val().trim(),
		status: $('select#phase').val(),
	};

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
		mira_search_results = response.results;

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
	results.sort((a,b)=>{return a.uptime['$date']-b.uptime['$date'];})
	results.forEach((o,i) => {

		o.thumb = atob(o.thumb['$binary']);

		let div = template.clone();
		div.removeAttr('data-template');
		div.attr('data-img', o._id['$oid']);
		div.show();

		div.find('#thumb').attr('src', o.thumb);
		div.find('#filename').text(o.filename);
		div.find('#uptime').text(moment(o.uptime["$date"]).calendar(null, {sameElse: 'DD/MMM/YYYY'}));
		div.find('#status').text(img_status[o.phase]);

		container.append(div);
	})

}



function mira_search_open(control) {

	let imgID = jQuery(control).closest('tr').attr('data-img');
	window.location.href = "/show/" + imgID;
}

/* ************************************************************************** */

/* *** IMAGE SHOW SYSTEM *** ************************************************ */
var mira_imagedata;

function mira_show_refresh() {

	$('.spinner').show();
	snackBar('refreshing...');

	$.getJSON('/show/'+imageID+'/refresh', { })
	.done(function(response) {
		
		console.log(response);
		snackBar(response.message, {error: response.type != 'success'});
		mira_imagedata = response;

		imagedata = response.image;
		mira_show();

		// if there is a task...
		if(response.task != null) {
			mira_show_check_cycle(response.task);
		} else {
			$('.spinner').hide();
		}
	});
}

function mira_show() {

	$('#phase').text(img_status[mira_imagedata.image.phase]);
	$('[scan-disable]').prop('disabled', mira_imagedata.task != null);

	mira_show_resize();
	mira_show_listcrops();
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
		if(typeof imagedata.crops === 'undefined') return;

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

	let container = $('#croplist tbody');
	let template = container.find('[data-template="crop"]');
	container.find('[data-crop]').remove();

	$('#croplist').hide();
	$('#cropinfo').hide();
	
	// for crops
	if(typeof imagedata.crops === 'undefined') return;
	if(imagedata.crops.length == 0) return;

	$('#croplist').show();	
	imagedata.crops.forEach((c,i) => {

		c.index = i;

		let div = template.clone();
		div.removeAttr('data-template');
		div.attr('data-crop', i);
		div.data('crop', c);

		let ML = c.analysis.find(o => o.name == 'Foxer');
		if(ML) {
			if(ML.result.empty > 0.5) div.find('#outputL').text('---');
			else {
				if(ML.result.fox > ML.result.skunk) div.find('#outputL').text('fox: ' + (ML.result.fox*100).toFixed(2) + '%');
				else div.find('#outputL').text('skunk: ' + (ML.result.skunk*100).toFixed(2) + '%');
			}
		}
		ML = c.analysis.find(o => o.name == 'ratter');
		if(ML) {
			if(ML.result.empty > 0.5) div.find('#outputS').text('---');
			else div.find('#outputS').text('rodent: ' + (ML.result.rodent*100).toFixed(2) + '%');
		}

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



function mira_show_cropdetails(control) {

	let div = $(control).closest('[data-crop]');
	let cropID = parseInt(div.attr('data-crop'));
	let cropinfo = div.data('crop');

	// redraw the image with crop
	mira_show_resize(cropID);


	$('[data-crop]').css('background', '');
	div.css('background', '#EEF');

	let template = $('#cropinfo [data-template="analysis"]');
	let container = $('#cropinfo');
	container.data('crop', cropinfo);
	container.find('[data-analysis]').remove();
	container.show();


	cropinfo.analysis.forEach((a) => {

		let adiv = template.clone();
		adiv.removeAttr('data-template');
		adiv.attr('data-analysis', '1');
		adiv.find('#model').text(a.name);
		adiv.find('#model').attr('title', a.fullname);

		let res = adiv.find('#results');
		let classes = Object.keys(a.result).sort();
		classes.forEach((cls) => {
			let spn = $(document.createElement('span'));
			let p = a.result[cls]*100;
			spn.text(cls+': '+ p.toFixed(2) + '%');
			res.append(spn);
		});

		adiv.show();
		adiv.insertBefore(template);
	});


}



function mira_show_override() {

	let container = $('#cropinfo');
	let cropinfo = container.data('crop');
	let cls = container.find('#classfixer').val();

	let request = {
		cropID: cropinfo.index,
		class: cls,
	};


	$('#btOverride').prop('disabled', true);


	$.ajax({
		url: '/show/'+imageID+'/override',
		data: JSON.stringify(request),
		contentType: 'application/json;charset=UTF-8',
		type: 'POST'
	})
	.done(function(resp) {
		let response = JSON.parse(resp);
		snackBar(response.message, {error: response.type != 'success'});
		mira_show_refresh();
	})
	.fail(function(xhr){
		snackBar('ŚERVER ERR0R', {error: true}); 
		console.log(xhr);
	})
	.always(function(){
		//$('.spinner').hide();
		$('#btOverride').prop('disabled', false);
	});
}





function mira_show_check_cycle(task) {

	let checkURL = '/check/' + task.ctask;

	// show a message in the footer
	let msg = task.msgwait;
	if(typeof task.msgwait === 'undefined') msg = 'background task running...';

	$.getJSON(checkURL, {}, function() {})
	.done(function(response) { // AJAX worked...

		console.log(response);

		if(response.type == 'NOTFOUND') {
			/*
			Notebook_stepmessage(stepdiv, '', false, false);
			Notebook_log(msender, 'task ['+task.task+'] not found on the server', 'warning', false);

			// TODO: issue a step/task update
			// there is problem here if the task somehow failed...
			// the server will not delete the task object from mongo
			// so the client cannot rerun it
			// however, the server might have deleted the task from celery, causing
			// this request to return NOTFOUND

			delete globalinfo.tasks[task.ctask]
			*/
			return;
		}


		if(response.type == 'SUCCESS') { 
			
			// task was completed, we should refresh the image
			mira_show_refresh();
			return;
		}


		if(response.type == 'FAILURE') {
			/*
			stepdiv.find('#footer #spinner').hide();
			stepdiv.find('#footer #error').text('background task failed');
			console.log('background task '+task.task+' failed'); console.log(task);
			//snackBar('SERVER ERROR!', {error: true});

			delete globalinfo.tasks[task.ctask];
			*/
			return;
		}

		// in any other case, we should check again
		setTimeout(function() {
			mira_show_check_cycle(task);
		}, 2000);

	})
	.fail(function(xhr) {
		snackBar('SERVER ERROR', {error: true});
		//Notebook_stepmessage(stepdiv, 'error checking background task', false, false);
		//Notebook_log(msender, 'error checking background task', 'error', true);
		console.log(xhr);
	});
}





function mira_show_delete() {

	window.location.href = '/show/delete/' + imageID;
}


/* ************************************************************************** */





