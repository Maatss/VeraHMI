<div style="position:absolute; top:0px; left:401px; bottom:0px; right:0px; overflow:scroll">
<table cellpadding="0" cellspacing="0" class="stdtable">
<tr>
<td>Time</td>
<td>Level</td>
<td>Module</td>
<td>Message</td>
</tr>
<?
include "../include/mysql.php";
$day = $_GET['day'];
$result = mysql_query("SELECT * FROM HMILog WHERE day='$day' ORDER BY id DESC") 
or die(mysql_error()); 
$bg = 0;
while($row = mysql_fetch_array( $result )) {
?>
<tr>
<td width="140px"><? echo $row['timestamp']; ?></td>
<td width="80px"><?
switch ($row['level']) {
 case 1 : echo "Trace";
 			break;
 case 2 : echo "Debug";
 			break;
 case 3 : echo "Warn";
 			break;
 case 4 : echo "Error";
 			break;
 case 5 : echo "Fatal";
 			break;
}
 ?></td>
<td width="100px"><? echo $row['module']; ?></td>
<td><? echo $row['msg']; ?></td>
</tr>
<?
}
?>
</table>
</div>