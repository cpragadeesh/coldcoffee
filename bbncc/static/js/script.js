function _submit(problem_id, w=500, h=500) {
	
	var left = (screen.width/2)-(w/2);
  	var top = (screen.height/2)-(h/2);
	console.log("width=100, height=100, top=" + top + ", left=" + left);
	return window.open("/submit/" + problem_id, "Submit", 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width='+w+', height='+h+', top='+top+', left='+left);
}

function _submit_source(problem_id, w=500, h=500) {

	var left = (screen.width/2)-(w/2);
  	var top = (screen.height/2)-(h/2);
	console.log("width=100, height=100, top=" + top + ", left=" + left);
	return window.open("/submit_source/" + problem_id, "Submit", 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width='+w+', height='+h+', top='+top+', left='+left);

}

function input_download(problem_id) {

	var reply = confirm("Timer will start when you press \"OK\". Are you sure you want to download?");

	if(reply == false) {
		return;
	}

	window.location.href = "/input-download/" + problem_id;

	show_submit_panel(problem_id);
}

var time_limit = 6;
var counter = time_limit * 60;

function show_submit_panel(problem_id) {

	container = document.getElementById("uploadcontainer");
	container.style.display = 'block';

	bttn = document.getElementById("input-download");
	if(bttn != null) {
		bttn.style.marginBottom = "30px";
		bttn.style.display = 'none';
	}
	
	setInterval(function() {
		counter--;

		var min = counter / 60;
		var sec = counter % 60;

		if(sec < 10) {
			sec = sec.toString();
			sec = '0' + sec;	
		}

		else {
			sec = sec.toString();
		}

		console.log(counter);
		if(counter < 0) {
			document.getElementById("countdown").innerHTML = "Time's up.";
		}

		else {
			document.getElementById("countdown").innerHTML = "0" + Math.floor(min).toString() + ":" + sec;
		}

	}, 1000);
}

function source_download(problem_id) {

	window.location.href = "/source-download/" + problem_id
}

function checkSubmit() {

	if(document.getElementById("id_source_file").files.length == 0 || document.getElementById("id_output_file").files.length == 0) {
		document.getElementById("error-row").innerHTML = "Please choose both files";
		return false;
	}

	else {
		document.getElementById("submit-button").click();
		return true;
	}
}