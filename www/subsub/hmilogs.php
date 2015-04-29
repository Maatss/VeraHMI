<?php
include "../include/mysql.php";

//$response = file_get_contents("http://localhost/actions/getXls.php");
$result = mysql_query("SELECT * FROM HMILog GROUP BY day ORDER BY day DESC") 
or die(mysql_error()); 
while($row = mysql_fetch_array( $result )) {
?>


<div class="subsubitem" id="subsub<? echo $row['id'] ?>" onClick="setActiveSubSubItem('subsub<? echo $row['id'] ?>');getData('hmilog','?day=<? echo $row['day']; ?>')"><? echo $row['day']; ?></div>
<div class="line"></div>
<?
}
?>


