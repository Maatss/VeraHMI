<?
include "../include/mysql.php";
$result = mysql_query("SELECT * FROM ECULogs ORDER BY timestamp DESC") 
or die(mysql_error()); 
while($row = mysql_fetch_array( $result )) {
?>
<div class="subsubitem" id="subsub<? echo $row['id'] ?>"  onClick="setActiveSubSubItem('subsub<? echo $row['id'] ?>');getRaceLog('?id=<? echo $row['id']; ?>')"><? echo $row['timestamp']; ?></div>
<div class="line"></div>
<?
}
?>