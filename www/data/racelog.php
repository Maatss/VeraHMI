<div style="position: absolute; top: 1px; left: 401px; bottom: 0px; right: 0px; overflow: scroll">
<div id="ECUData">
<?
include "../include/mysql.php";
$id = $_GET['id'];
$result = mysql_query("SELECT * FROM ECULog".$id) or die(mysql_error()); 

echo "Ingtime,Ingpos,Injpos,Injtime\n";

while($row = mysql_fetch_array( $result )) {
echo $row['ign_time'].","; 
echo $row['ign_pos'].","; 
echo $row['inj_pos'].","; 
echo $row['inj_time']; 
echo "\n";
}
?>
</div>
<div id="mychart"></div>
</div>