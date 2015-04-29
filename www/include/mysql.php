<?
$mysql_user = "root";
$mysql_pass = "verateam";
$mysql_host = "localhost";

mysql_connect($mysql_host, $mysql_user, $mysql_pass) or die(mysql_error());
mysql_select_db("Vera") or die(mysql_error());
?>