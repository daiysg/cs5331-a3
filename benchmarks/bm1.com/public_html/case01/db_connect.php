<?php

define('HOST', 'localhost');
define('DB_NAME', 'benchmarks');
define('DB_USER', 'root');
define('DB_PASSWORD', 'user');
define('USER_TABLE', 'users');
define('MESSAGES_TABLE', 'messages'); 

$conn = new mysqli(HOST, DB_USER, DB_PASSWORD, DB_NAME);
if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}

