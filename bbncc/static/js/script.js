function input_download(problem_id) {

	var time_limit = 8; //in mins

	var reply = confirm("Your input file will start download when you click 'OK'. Also a timer will start ticking, Upload your source" 
		+ " and output before the timer runs out. Do not close the tab or the window.");

	if(reply == false) {
		return;
	}

	window.open("/input-download/" + problem_id, "_blank");

	counter = time_limit * 60;

	container = document.getElementById("uploadcontainer");
	container.style.display = 'block';

	textcontainer = document.getElementById("problemtext");
	textcontainer.style.marginTop = "140px";

	bttn = document.getElementById("input-download");
	bttn.style.marginBottom = "30px";
	bttn.disabled = true;

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

		if(counter < 0) {
			document.getElementById("countdown").innerHTML = "Time's up.";
		}

		else {
			document.getElementById("countdown").innerHTML = "0" + Math.floor(min).toString() + ":" + sec;
		}

	}, 1000);
}

function source_download(problem_id) {

	window.open("/source-download/" + problem_id)
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