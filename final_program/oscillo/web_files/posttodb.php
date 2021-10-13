<?php

// REPLACE with your Server name
$servername = "db5004262074.hosting-data.io";
// REPLACE with your Database name
$dbname = "dbs3533657";
// REPLACE with Database user
$username = "dbu445238";
// REPLACE with Database user password
$password = "x81500jujua";

//print_r($_POST);

if ((!isset($_POST["reset"])) and 
	(!isset($_POST["autoscale"])) and 
	(!isset($_POST["savescreen"])) and 
	(!isset($_POST["savewaveform"])) and 
	(!isset($_POST["vertscale"])) and 
	(!isset($_POST["vertoffset"])) and 
	(!isset($_POST["horiscale"])) and 
	(!isset($_POST["horioffset"])) and 
	(!isset($_POST["trigedgelevel"])) and 
	(!isset($_POST["aqumode"])) and 
	(!isset($_POST["submit"])) and 
	(!isset($_POST["waveform"])) and 
	(!isset($_POST["error"])) and
	(!isset($_POST["screen_img"]))){
	die("POST variable is empty :(\n");
} else {
  $sqlData = ""; // data to insert in the UPDATE SQL command (string format)
  $first = 1; // variable to check if it's the first parameter that is not empty (so we don't place a ',' before)
  // checking each parameter if it's not set or empty, and if it's not the case, we insert it in the sqlData string
  if (isset($_POST["reset"]) and ($_POST["reset"] != '')) {
    $sqlData .= ",`reset`=" . $_POST["reset"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["autoscale"]) and ($_POST["autoscale"] != '')) {
    $sqlData .= ",`autoscale`=" . $_POST["autoscale"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["savescreen"]) and ($_POST["savescreen"] != '')) {
    $sqlData .= ",`savescreen`=" . $_POST["savescreen"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["savewaveform"]) and ($_POST["savewaveform"] != '')) {
    $sqlData .= ",`savewaveform`=" . $_POST["savewaveform"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["vertscale"]) and ($_POST["vertscale"] != '')) {
    $sqlData .= ",`vertscale`=" . $_POST["vertscale"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["vertoffset"]) and ($_POST["vertoffset"] != '')) {
    $sqlData .= ",`vertoffset`=" . $_POST["vertoffset"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["horiscale"]) and ($_POST["horiscale"] != '')) {
    $sqlData .= ",`horiscale`=" . $_POST["horiscale"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["horioffset"]) and ($_POST["horioffset"] != '')) {
    $sqlData .= ",`horioffset`=" . $_POST["horioffset"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["trigedgelevel"]) and ($_POST["trigedgelevel"] != '')) {
    $sqlData .= ",`trigedgelevel`=" . $_POST["trigedgelevel"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["aqumode"]) and ($_POST["aqumode"] != '')) {
    $sqlData .= ",`aqumode`=" . $_POST["aqumode"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["submit"]) and ($_POST["submit"] != '')) {
    $sqlData .= ",`submit`=" . $_POST["submit"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["waveform"]) and ($_POST["waveform"] != '')) {
    $sqlData .= ",`waveform`=\"" . $_POST["waveform"] . '"';
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["error"]) and ($_POST["error"] != '')) {
    $sqlData .= ",`error`=" . $_POST["error"];
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
  if (isset($_POST["screen_img"]) and ($_POST["screen_img"] != '')) {
	$sqlData .= ",`screen_img`=\"" . $_POST["screen_img"] . '"';
    if ($first==1) {
      $sqlData = substr($sqlData, 1);
      $first = 0;
    }
  }
}

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}

// Update of the table oscillo
$sql = "UPDATE `oscillo` SET " . $sqlData . " WHERE `id`=1";
if ($conn->query($sql) === TRUE) {	// sending the SQL command
  echo "Update made successfully \n"; // if there is no error
} 
else {
  echo "Error: " . $sql . "<br>" . $conn->error . "\n"; // if there is an error
}

// mySQL request example : UPDATE `exp1` SET `start`=3,`tempMeas`=3 WHERE `id`=1
