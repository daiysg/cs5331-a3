<?php 
    session_start();
    if (empty($_SESSION['id'])) {
        header("Location: login.php"); 
    }
    include_once 'db_connect.php'; 
    $sql = "SELECT m.id AS id, title, content, u.username AS username FROM " . MESSAGES_TABLE . " m, " .
           USER_TABLE . " u WHERE u.id = m.user"; 
    $result = $conn->query($sql); 
     
    $error_message = ""; 
    if ( $_SERVER['REQUEST_METHOD'] == 'POST' ) { 
        if ( !empty($_POST['title']) and !empty($_POST['content']) ) { 
            if (!empty($_POST[$_SESSION['CSRFName']]) && ($_POST[$_SESSION['CSRFName']] == $_SESSION['CSRFToken'])) {
                $title_value = $_POST['title']; 
                $content_value = $_POST['content']; 
             
                $query = $conn->prepare("INSERT INTO ".MESSAGES_TABLE."(title, content, user) VALUES (?, ?, ?)"); 
                $query->bind_param("sss", $title_value, $content_value, $_SESSION['id']); 
                $query->execute(); 
                header("Location: " . $_SERVER['REQUEST_URI']);
            } else {
            	$error_message = "Invalid CSRF Token.";
            }
        }else{ 
            $error_message = "Please ensure both fields are filled."; 
        } 
    } 
     
    if (isset($_GET['delete']) && ($_GET['delete'] == 'true')) { 
	if (isset($_GET[$_SESSION['CSRFName']]) && ($_GET[$_SESSION['CSRFName']] == $_SESSION['CSRFToken'])) {
            if ($_SESSION['isAdmin']){ 
                $sql2 = "DELETE FROM ".MESSAGES_TABLE. " WHERE id >= 1"; 
                $result2 = $conn->query($sql2); 
             
                $sql3= "ALTER TABLE ".MESSAGES_TABLE." AUTO_INCREMENT = 1;"; 
                $result3 = $conn->query($sql3); 
                header("Location: " . $_SERVER["PHP_SELF"]); 
            } else {
 	        $del_error_message = "You are not an admin.";
	    }
        } else {
	    $del_error_message = "Invalid CSRF Token.";
        }
         
    } 
    $conn->close(); 
     
?> 
<!DOCTYPE html>
<html>
<head>
	<title>Messages</title>
	<meta charset="UTF-8"> 
    <script> 
    var tagsToReplace = { 
        '&': '&amp;', 
        '<': '&lt;', 
        '>': '&gt;' 
    }; 
     
    function replaceTag(tag) { 
        return tagsToReplace[tag] || tag; 
    } 
     
    function safe_tags_replace(str) { 
        return str.replace(/[&<>]/g, replaceTag); 
    } 
     
    function sanitise(){ 
        var input = document.getElementById('title').value; 
        input = safe_tags_replace(input);  
        document.getElementById('title').value = input; 
         
        var input2 = document.getElementById('content').value; 
        input2 = safe_tags_replace(input2);  
        document.getElementById('content').value = input2; 
         
        document.getElementById("form_valid").submit(); 
    } 
     
    </script> 
</head>
    <body> 
        <h1>Messages</h1> 
        Welcome, <?php echo $_SESSION['user']?>! Click <a href="logout.php">here</a> to logout.<br/>
        <font color=red>[Admin Users Only] To delete all messages, click <a href="?delete=true&<?php echo $_SESSION['CSRFName'] . '=' . $_SESSION['CSRFToken']; ?>">here</a>. </font><br/><br/> 
         <?php 
            if(!empty($del_error_message)){ 
                echo "<font color='red'>".$del_error_message."</font><br/><br/>"; 
            } 
        ?> 
	
        <h3>Guest Book</h3> 
        <?php 
            if ($result->num_rows > 0) { 
                while($row = $result->fetch_assoc()) { 
                    echo $row["id"]. ". " . $row["title"]. " (Posted by <i>" . $row["username"] ."</i>)<br/>" . $row["content"]."\n"; 
                    echo "<br/><br/><br/>\n\n"; 
                } 
            }  
        ?> 
         
     
        <br/><br/><br/> 
        <?php 
            if(!empty($error_message)){ 
                echo "<font color='red'>".$error_message."</font>"; 
            } 
        ?> 
         
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post" id="form_valid" enctype="multipart/form-data">  
            Enter your comments:  
            <table> 
                <tr> 
                    <td width="20%">Title: </td> 
                    <td><input type="type" id="title" name="title" maxlength="10"/><br/><br/></td> 
                </tr> 
                 
                <tr> 
                    <td>Message: </td> 
                    <td><textarea name="content" id="content" cols="50" rows="10"></textarea><br/><br/></td> 
                </tr> 
            </table> 
 	    <input type="hidden" name="<?php echo $_SESSION['CSRFName']; ?>" value="<?php echo $_SESSION['CSRFToken']; ?>">
            <input type="submit" onClick="sanitise()"/> 
        </form> 
         
        <br/>         
    </body> 
</html>
