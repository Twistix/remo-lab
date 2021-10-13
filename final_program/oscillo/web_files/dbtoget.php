<?php

/*
  file description
*/

// REPLACE with your Server name
$servername = "db5004262074.hosting-data.io";
// REPLACE with your Database name
$dbname = "dbs3533657";
// REPLACE with Database user
$username = "dbu445238";
// REPLACE with Database user password
$password = "x81500jujua";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}

// Perform query
$sql = "SELECT reset, autoscale, savescreen, savewaveform, vertscale, vertoffset, horiscale, horioffset, trigedgelevel, aqumode, submit, waveform, error, screen_img FROM `oscillo` WHERE `id`=1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    echo $row["reset"]. ";" 
      . $row["autoscale"]. ";" 
      . $row["savescreen"]. ";" 
      . $row["savewaveform"]. ";" 
      . $row["vertscale"]. ";"
      . $row["vertoffset"]. ";"
      . $row["horiscale"]. ";"
      . $row["horioffset"]. ";"
      . $row["trigedgelevel"]. ";"
      . $row["aqumode"]. ";"
      . $row["submit"]. ";"
      . $row["waveform"]. ";"
      . $row["error"]. ";"
      . $row["screen_img"] ;
  }
} else {
  echo "0 results";
}

// mySQL request example : UPDATE `exp1` SET `start`=3,`tempMeas`=3 WHERE `id`=1
