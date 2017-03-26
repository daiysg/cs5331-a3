<?php 
    session_start();
    include_once 'db_connect.php'; 
    if ( $_SERVER['REQUEST_METHOD'] == 'POST' ) { 
        if ( !empty($_POST['username']) && !empty($_POST['password']) ) { 
            $user = htmlspecialchars($_POST['username']); 
            $password = md5($_POST['password']); 
	    $sql = "SELECT id, isAdmin FROM " . USER_TABLE . " WHERE username=? AND password=?";
            $query = $conn->prepare($sql);
            $query->bind_param("ss", $user, $password); 
    	    $query->execute();
	    $query->bind_result($id, $isAdmin);
	    while ($query->fetch()) {
	    	session_start();
                $_SESSION['id'] = $id;
		$_SESSION['user'] = $user;
		$_SESSION['isAdmin'] = $isAdmin;
		header("Location: messages.php"); 
	    }
            $error_message = "Invalid username/password combination."; 
	} else {
	    $error_message = "Please enter both your username and password."; 
        }
    } 
?>
<!DOCTYPE html>
<html>
<head>
	<title>Login</title>
	<meta charset="UTF-8"> 
</head>
<body>
    <?php 
        if(!empty($error_message)){ 
            echo "<font color='red'>".$error_message."</font>"; 
        } 
    ?> 
	<form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post" name="login_form" enctype="multipart/form-data">
		Username : <input type="text" name="username" />
		Password : <input type="password" name="password" />
		<input type="submit" value="Login" name="submit">
	</form>

</body>
