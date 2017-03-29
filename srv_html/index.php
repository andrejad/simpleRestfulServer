<?php 

session_start();

if (!isset($restSrvUrl)) { 
  $publicIp = trim(shell_exec("curl -s http://whatismyip.akamai.com/"));  
  $restSrvUrl = 'http://' . $publicIp . ':5000';  
}

$trgphp = htmlspecialchars($_SERVER['PHP_SELF']);

function test_input($data) {

  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
};

function CallAPI($url, $data) {

  #print "</br>url:" . $url;
  #print "</br>data:" . $data;
  // // $data = http_build_query( $data ); //not needed!
  $context = array(
      'http' => array(
              'protocol_version' => 1.1,
              'method'    =>  'PUT',
              'header'    =>  
              //"Authorization: apikeystring\r\n" . "Content-Length: " . strlen( $data ) . "\r\n". //not needed for now
              "Content-Type: application/json",
              'content'   =>  $data
          )                             
      );

  $context = stream_context_create( $context );
  
  $result = file_get_contents( $url, false, $context );
  print "</br>RESULT=" . $result;
  return $result;
}

// define variables and set to empty values
$actionId = $owner = $taskid = $priority = $msg = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  
  $actionId = test_input($_POST["actionId"]);
  $owner = test_input($_POST["owner"]);
  $taskid = test_input($_POST["taskid"]);
  $priority = test_input($_POST["priority"]);
  $msg = test_input($_POST["msg"]);
  $newUri = test_input($_POST["resturl"]);

  $datamap = array();
  $datamap['message'] = $msg;
  $datamap['priority'] = $priority;
  $datamap['owner'] = $owner;
  $datamap['taskId'] = $taskid;
  
  $json = json_encode($datamap, JSON_FORCE_OBJECT);

  if (count($json)<1) { $json = ""; }

  if ($actionId == 'newtask') {    
    echo "</br>clicked on newtask";
    unset($datamap[taskId]);
    $url = $restSrvUrl . '/new';
    CallAPI($url, $json);

  } elseif ($actionId == 'edittask') {
    $url = $restSrvUrl . '/update';
    CallAPI($url, $json);

  } elseif ($actionId == 'deltask') {
    $results = file_get_contents($restSrvUrl . "/del/" . $taskid);
    echo $results;

  } elseif ($actionId == 'changeUrl') {
    $restSrvUrl = $newUri;

  } elseif ($actionId == 'alldata') {
    $results = file_get_contents($restSrvUrl . "/alldata");
    $_SESSION['jresults'] = $results;;
    include_once "shwj.php";
    goto skiptoend;
    
  } elseif ($actionId == 'getByOwner') {
    $results = file_get_contents($restSrvUrl . '/owner/' . $owner);
    $_SESSION['jresults'] = $results;;
    include_once "shwj.php";
    goto skiptoend;
  
  } else {
      echo "Action not supported";

  };

};

?>

<html>
<body>

<form method="post" action="<?=$trgphp;?>">
<button type="submit">Change REST</button><input type="text" name="resturl" value="<?php echo $restSrvUrl; ?>" >
<input type="hidden" name="actionId" value="changeUrl">
</form>

<form method="post" action="index.php">
<button type="submit">Display all data</button>
<input type="hidden" name="actionId" value="alldata">
<button TYPE="button" onClick="parent.location='<?php echo $restSrvUrl ?>/'">All API</button>
</form>


<h3>Add new task</h3>

<form method="post" action="<?php echo $trgphp; ?>">
Owner: <input type="text" name="owner"><br>
Priority: <input type="text" name="priority"><br>
Message: <input type="text" name="msg"><br>
<input type="hidden" name="actionId" value="newtask">
<button type="submit">Add new</button>
</form>

<br>

<h3>Modify task</h3>

<form method="post" action="<?php echo $trgphp; ?>">
ID: <input type="text" name="taskid"><br>
Owner: <input type="text" name="owner"><br>
Priority: <input type="text" name="priority"><br>
Message: <input type="text" name="msg"><br>
<input type="hidden" name="actionId" value="edittask">
<button type="submit">Modify</button>
</form>

<h3>Search by owner</h3>
<form method="post" action="<?php echo $trgphp; ?>">
Owner: <input type="text" name="owner"><br>
<input type="hidden" name="actionId" value="getByOwner">
<button type="submit">Search</button>
</form>

<h3>Remove task</h3>
<form method="post" action="<?php echo $trgphp; ?>">
ID: <input type="text" name="taskid"><br>
<input type="hidden" name="actionId" value="deltask">
<button type="submit">Delete</button>
</form>

</body>
</html>

<?php
skiptoend:
?>