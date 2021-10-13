// ===================================== VARIABLES =============================================
// variables linked to the document
var btnReset = document.getElementById("btnReset");
var btnAutoscale = document.getElementById("btnAutoscale");
var btnSubmit = document.getElementById("btnSubmit");
var btnSscreen = document.getElementById("btnSscreen");
var btnSwaveform = document.getElementById("btnSwaveform");

// variables of the database to be shared with the local node program
var reset = 0;
var autoscale = 0;
var saveScreen = 0;
var saveWaveform = 0;
var submit = 0;
var waveform = "";
var config = "";
var error = 0;
var screen_img = "";
  
// ======================================= GET FUNCTION =============================================
// This function makes a GET request to the url specified in it. The mode used is asynchronous, so a non blocking mode.
// When the get request succeed, a callback function is called to perform some actions with the result of the request.
// Actions to be performed when the request is finished can also be directly coded into this function (under if (xhr.status === 200))
// The function takes in argument a function (callback function)
function httpGet(callback) {
var xhr = new XMLHttpRequest(); 	// creation of an object XMLHttpRequest
xhr.onreadystatechange = (e) => { 	// onreadystatechange is un event depending on when the state of the request change
  if (xhr.readyState !== 4) { 	// "if the requenst isn't finished yet
	return;
  }
  if (xhr.status === 200) { 	// "if the request is done and if she succeed" then we can perform some actions (ex : call a callback function)
	// actions that are performed when the request is finished
	console.log('SUCCESS', xhr.responseText);
	var getStr = new String(xhr.responseText);	// result of the get request (see dbtoget.php file)
	var index = [];	// creation of an array index
	var curr = 0;	// current position in the get string
	var nbSeparator = 13; // number of separators with the dbtoget.php file
	for (let i = 0; i < nbSeparator; i++) {	// there we parcour all the get string and we save the indexes where we find a ";" character
	  curr = getStr.indexOf(";",curr+1);
	  index.push(curr);
	}
	// then we can slice the get string in differents part with the indexes founds previously and then update the variables (defined outside the function)
	reset = getStr.slice(0, index[0]);
	autoscale = getStr.slice(index[0]+1, index[1]);
	saveScreen = getStr.slice(index[1]+1, index[2]);
	saveWaveform = getStr.slice(index[2]+1, index[3]);
	submit = getStr.slice(index[9]+1, index[10]);
	waveform = getStr.slice(index[10]+1, index[11]);
	error = getStr.slice(index[11]+1, index[12]);
	screen_img = getStr.substring(index[12]+1);
	callback();		// callback function passed in argument of the function httpGet
  } else {
	console.warn('request_error');	// if the status isn't 200 the there is an error in the request
  }
}
xhr.open( "GET", "https://idee3d.xyz/remolab/oscilloscope/dbtoget.php", true);	//we lunch a get request in asynchronous mode at the url idee3d.xyz/remolab...
xhr.send(); // we send nothing with the get request there
}

// ======================================= POST FUNCTION =============================================
// This function makes a POST request to the url specified in it. The mode used is asynchronous, so a non blocking mode.
// When the post request succeed, a callback function is called to perform some actions.
// Actions to be performed when the request is finished can also be directly coded into this function (under if (xhr.status === 200))
// The function takes in argument a function (callback function) and a FormData object (like a dictionnary in other languages)
function httpPost(data, callback)
{
var xhr = new XMLHttpRequest();		// creation of an object XMLHttpRequest
xhr.onreadystatechange = (e) => {	// onreadystatechange is un event depending on when the state of the request change
  if (xhr.readyState !== 4) {	// "if the requenst isn't finished yet
	return;
  }
  if (xhr.status === 200) {		// "if the request is done and if she succeed" then we can perform some actions (ex : call a callback function)
  // actions that are performed when the request is finished
	console.log('SUCCESS', xhr.responseText);
	callback();		// callback functions passed in argument of the function httpPost
  } else {
	console.warn('request_error');
  }
}
xhr.open( "POST", "https://idee3d.xyz/remolab/oscilloscope/posttodb.php", true);	//we lunch a post request in asynchronous mode at the url idee3d.xyz/remolab...
xhr.send(data);	// we send the data through the post request
}


// ======================================= FAUTOSCALE FUNCTION =============================================
// This is the function that is lunched when the user click on the autoscale button
// It takes no arguments and return nothing
function fautoscale()
{
let data = new FormData();
data.append('autoscale', 1);
btnAutoscale.disabled = true;	// we disable the autoscale button until the operation on the local node is finished (while the autoscale database variable equals 1)
httpPost(data,auto_loop);	// we launch a post request to set the autoscale database variable to 1 with the callback function auto_loop()
function auto_loop() {	// this function is automaticaly launched when the previous post request finished 
  httpGet(auto_loop2);	// we launch a get request to updates the variables of the javascript program to see if the autoscale has gone back to 0 (callback function = auto_loop2())
  function auto_loop2() {	// this function is automaticaly launched when the previous get request finished
	if (autoscale == 1 || error == 1) {	// if the autoscale variable is still 1, we relaunch auto_loop2 with a delay of 500ms to perform a new get request, and so on...
	  if (error == 1) { document.getElementById('txtError').innerHTML = "!!! ERROR !!! (reset in progress)"; }
	  setTimeout(function() {httpGet(auto_loop2);}, 1000);
	} else {
	  document.getElementById('txtError').innerHTML = "";
	  btnAutoscale.disabled = false;	// if the autoscale variable = 0, the the autoscale has finished on the local node and we re-enable the autoscale button
	}
  }
}
}

// ======================================= FRESET FUNCTION =============================================
// This is the function that is lunched when the user click on the reset button
// It takes no arguments and return nothing
function freset()
{
let data = new FormData();
data.append('reset', 1);
btnReset.disabled = true;	// we disable the reset button until the operation on the local node is finished (while the reset database variable equals 1)
httpPost(data,reset_loop);	// we launch a post request to set the reset database variable to 1 with the callback function reset_loop()
function reset_loop() {		// this function is automaticaly launched when the previous post request finished 
  httpGet(reset_loop2);		// we launch a get request to updates the variables of the javascript program to see if the reset has gone back to 0 (callback function = reset_loop2())
  function reset_loop2() {	// this function is automaticaly launched when the previous get request finished
	if (reset == 1 || error == 1) {		// if the reset variable is still 1, we relaunch reset_loop2 with a delay of 500ms to perform a new get request, and so on...
	  if (error == 1) { document.getElementById('txtError').innerHTML = "!!! ERROR !!! (reset in progress)"; }
	  setTimeout(function() {httpGet(reset_loop2);}, 1000);
	} else {
	  document.getElementById('txtError').innerHTML = "";
	  btnReset.disabled = false;	// if the reset variable = 0, the the reset has finished on the local node and we re-enable the reset button	
	}
  }
}
}

// ======================================= FSAVESCREEN FUNCTION =============================================
// This is the function that is lunched when the user click on the savescreen button
// It takes no arguments and return nothing
function fsavescreen()
{
let data = new FormData();
data.append('savescreen', 1);
btnSscreen.disabled = true;	// we disable the savescreen button until the operation on the local node is finished (while the savescreen database variable equals 1)
httpPost(data,ss_loop);	// we launch a post request to set the savescreen database variable to 1 with the callback function ss_loop()
function ss_loop() {	// this function is automaticaly launched when the previous post request finished 
  httpGet(ss_loop2);	// we launch a get request to updates the variables of the javascript program to see if the savescreen has gone back to 0 (callback function = ss_loop2())
  function ss_loop2() {	// this function is automaticaly launched when the previous get request finished
	if (saveScreen == 1 || error == 1) {	// if the savescreen variable is still 1, we relaunch ss_loop2 with a delay of 500ms to perform a new get request, and so on...
	  if (error == 1) { document.getElementById('txtError').innerHTML = "!!! ERROR !!! (reset in progress)"; }
	  setTimeout(function() {httpGet(ss_loop2);}, 1000);
	} else {
	  document.getElementById("screenImg").src = "data:image/png;base64,"+screen_img; // changing the screen image on the UI
	  document.getElementById('txtError').innerHTML = "";
	  btnSscreen.disabled = false;	// if the savescreen variable = 0, the the saving of the screen has finished on the local node and we re-enable the savescreen button
	}
  }
}
}

// ======================================= FSAVEWAVEFORM FUNCTION =============================================
// This is the function that is lunched when the user click on the savewaveform button
// It takes no arguments and return nothing
function fsavewaveform()
{
let data = new FormData();
data.append('savewaveform', 1);
btnSwaveform.disabled = true;	// we disable the savewaveform button until the operation on the local node is finished (while the savewaveform database variable equals 1)
httpPost(data,sw_loop);	// we launch a post request to set the savewaveform database variable to 1 with the callback function sw_loop()
function sw_loop() {	// this function is automaticaly launched when the previous post request finished 
  httpGet(sw_loop2);	// we launch a get request to updates the variables of the javascript program to see if the savewaveform has gone back to 0 (callback function = sw_loop2())
  function sw_loop2() {	// this function is automaticaly launched when the previous get request finished
	if (saveWaveform == 1 || error == 1) {	// if the savewaveform variable is still 1, we relaunch sw_loop2 with a delay of 500ms to perform a new get request, and so on...
	  if (error == 1) { document.getElementById('txtError').innerHTML = "!!! ERROR !!! (reset in progress)"; }
	  setTimeout(function() {httpGet(sw_loop2);}, 1000);
	} else {
	  download("waveform.txt", waveform);	// starting the download of the waveform as a txt file
	  document.getElementById('txtError').innerHTML = "";
	  btnSwaveform.disabled = false;	// if the savewaveform variable = 0, the the saving of the waveform has finished on the local node and we re-enable the savewaveform button
	}
  }
}
}

// ======================================= FSUBMIT FUNCTION =============================================
// This is the function that is lunched when the user click on the submit button
// It will update the different variables to be readed by the node on the database (ex an offset value for the oscilloscope)
// It takes no arguments and return nothing
function fsubmit()
{
let data = new FormData();
data.append('vertscale', document.getElementById('vertScale').value);	//we append the data to the FormData object (each row of FormData = key + value)
data.append('vertoffset', document.getElementById('vertOffset').value);
data.append('horiscale', document.getElementById('horiScale').value);
data.append('horioffset', document.getElementById('horiOffset').value);
data.append('trigedgelevel', document.getElementById('trigEdgelevel').value);
data.append('aqumode', document.getElementById('aqumode').value);
data.append('submit', 1);
btnSubmit.disabled = true;	// we disable the submit button until the operation on the local node is finished (while the submit database variable equals 1)
httpPost(data,submit_loop);	// we launch a post request with 
function submit_loop() {	// this function is automaticaly launched when the previous post request finished 
  httpGet(submit_loop2);	// we launch a get request to updates the variables of the javascript program to see if the submit has gone back to 0 (callback function = submit_loop2())
  function submit_loop2() {	// this function is automaticaly launched when the previous get request finished
	if (submit == 1 || error == 1) {		// if the submit variable is still 1, we relaunch submit_loop2 with a delay of 500ms to perform a new get request, and so on...
	  if (error == 1) { document.getElementById('txtError').innerHTML = "!!! ERROR !!! (reset in progress)"; }
	  setTimeout(function() {httpGet(submit_loop2);}, 1000);
	} else {
	  document.getElementById('txtError').innerHTML = "";
	  btnSubmit.disabled = false;	// if the submit variable = 0, we finished to submit the variables to the local node and we re-enable the submit button
	}
  }
}
}

// ======================================== DOWNLOAD FUNCTION =============================================
function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}





  
//UPDATE `oscillo` SET `reset`=0,`autoscale`=0, `submit`=0, `savewaveform`=0, `saveconfig`=0 WHERE `id`=1
