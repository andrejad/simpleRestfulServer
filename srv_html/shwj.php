<script type="text/javascript">
  setInterval("my_function();",5000); 
 
    function my_function(){
        window.location = location.href;
    }
</script>

<?php

session_start();
#$result = json_decode($_SESSION['jresults']);
$result = json_decode(file_get_contents($_SESSION['restSrvUrl'] . "/alldata"));

?>

<!--<a href="<?php echo $_SERVER['REQUEST_URI']; ?>">return</a>-->
<a href="<?php echo  $_SESSION['baseIp'].'/index.php'; ?>">return</a>

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
    
