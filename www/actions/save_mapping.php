<?
ini_set('set_time_limit', 50);
$indata = str_replace(",","+",$_GET["data"]);
$indata = str_replace("undefined","0",$indata);
$indata = substr($indata, 0, -1);

$data = shell_exec('sudo /usr/bin/python writeNoResponse.py 2 '.$_GET["id"].' '.$indata);
echo $data;
?>