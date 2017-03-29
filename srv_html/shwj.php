<?php

session_start();
$result = json_decode($_SESSION['jresults']);

?>

<a href="<?php echo $_SERVER['REQUEST_URI']; ?>">return</a>

<h2>Results:</h2>
    <?php for ($i=0; $i < count($result); $i++) { ?>
    	<table border=1>
    	<tr bgcolor="#DDDDDD"><td>ID</td><td><?=$result[$i]->rowId;?></td></tr>
	    <tr><td>Timestamp</td><td><?=$result[$i]->timestamp;?></td></tr>	    
	    <tr><td>Owner</td><td><?=$result[$i]->owner;?></td></tr>
	    <tr><td>Priority</td><td><?=$result[$i]->priority;?></td></tr>
	    <tr><td>Message</td><td><?=$result[$i]->message;?></td></tr>
	    </table>
	    </br>
    <?php 
	}
?>
    
